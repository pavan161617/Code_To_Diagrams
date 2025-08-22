from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ast
import re

app = FastAPI()

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code_snippet: str
    language: str  # "python", "java", "c"

@app.post("/generate-diagram/")
async def generate_diagram(request: CodeRequest):
    code = request.code_snippet
    lang = request.language.lower()

    if lang == "python":
        return {
            "flowchart": generate_flowchart_python(code),
            "sequence": generate_sequence_python(code),
            "state": generate_state_machine_python(code),
            "class": generate_class_diagram_python(code),
        }
    elif lang in ["java", "c"]:
        parsed = parse_java_c(code)
        return {
            "flowchart": generate_flowchart_java_c(parsed),
            "sequence": generate_sequence_java_c(parsed),
            "state": generate_state_machine_java_c(parsed),
            "class": generate_class_diagram_java_c(parsed),
        }
    else:
        return {"error": f"Unsupported language: {lang}"}


# -------------------------
# PYTHON DIAGRAMS
# -------------------------
def generate_flowchart_python(code: str) -> str:
    try:
        tree = ast.parse(code)
        diagram = ["flowchart TD"]
        counter = {"count": 0}

        def new_node(label: str, shape="process"):
            counter["count"] += 1
            safe_label = re.sub(r'[^a-zA-Z0-9_ ><=]', '', label)
            node_id = f"N{counter['count']}"
            if shape == "decision":
                return f"{node_id}{{{safe_label}}}"
            elif shape == "io":
                return f"{node_id}[/ {safe_label} /]"
            elif shape == "terminator":
                return f"{node_id}(({safe_label}))"
            return f"{node_id}[{safe_label}]"

        def walk(node, prev_node):
            if isinstance(node, ast.FunctionDef):
                func_node = new_node(f"Function: {node.name}", "terminator")
                diagram.append(f"{prev_node} --> {func_node}")
                last = func_node
                for stmt in node.body:
                    last = walk(stmt, last)
                return last

            elif isinstance(node, ast.If):
                cond_node = new_node(f"If {ast.unparse(node.test)}", "decision")
                diagram.append(f"{prev_node} --> {cond_node}")

                # True branch
                last_true = cond_node
                for stmt in node.body:
                    last_true = walk(stmt, last_true)

                # False branch (handle elif / else)
                last_false = cond_node
                for stmt in node.orelse:
                    last_false = walk(stmt, last_false)

                merge_node = new_node("Merge")
                diagram.append(f"{last_true} --> {merge_node}")
                diagram.append(f"{last_false} --> {merge_node}")
                return merge_node

            elif isinstance(node, (ast.For, ast.While)):
                loop_node = new_node(f"Loop: {ast.unparse(node)}", "decision")
                diagram.append(f"{prev_node} --> {loop_node}")
                last = loop_node
                for stmt in node.body:
                    last = walk(stmt, last)
                diagram.append(f"{last} --> {loop_node}")  # loop back
                return loop_node

            elif isinstance(node, ast.Return):
                ret_node = new_node(f"Return: {ast.unparse(node.value)}", "io")
                diagram.append(f"{prev_node} --> {ret_node}")
                return ret_node

            elif isinstance(node, ast.Assign):
                assign_node = new_node(f"Assign: {ast.unparse(node)}", "process")
                diagram.append(f"{prev_node} --> {assign_node}")
                return assign_node

            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                call_node = new_node(f"Call: {ast.unparse(node.value)}", "process")
                diagram.append(f"{prev_node} --> {call_node}")
                return call_node

            return prev_node

        last_node = new_node("Start", "terminator")
        for node in tree.body:
            last_node = walk(node, last_node)
        end_node = new_node("End", "terminator")
        diagram.append(f"{last_node} --> {end_node}")

        return "\n".join(diagram)

    except Exception as e:
        return f"%% Error parsing Python code: {str(e)}"


def generate_sequence_python(code: str) -> str:
    try:
        tree = ast.parse(code)
        lifelines = set()
        messages = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                lifelines.add(node.name)
                for stmt in node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                        callee = ast.unparse(stmt.value.func)
                        lifelines.add(callee)
                        messages.append((node.name, callee))
        diagram = ["sequenceDiagram"]
        for ll in lifelines:
            diagram.append(f"participant {re.sub(r'[^a-zA-Z0-9_]', '', ll)}")
        for caller, callee in messages:
            diagram.append(f"{re.sub(r'[^a-zA-Z0-9_]', '', caller)} ->> {re.sub(r'[^a-zA-Z0-9_]', '', callee)}: call")
        return "\n".join(diagram)
    except Exception as e:
        return f"%% Error parsing Python code: {str(e)}"


def generate_state_machine_python(code: str) -> str:
    try:
        tree = ast.parse(code)
        diagram = ["stateDiagram-v2", "[*] --> Start"]

        def walk(node, current):
            if isinstance(node, ast.FunctionDef):
                state = re.sub(r'[^a-zA-Z0-9_]', '', node.name)
                diagram.append(f"state {state}")
                diagram.append(f"{current} --> {state}: enter {state}")
                for stmt in node.body:
                    walk(stmt, state)

            elif isinstance(node, ast.If):
                cond = re.sub(r'[^a-zA-Z0-9_ ><=]', '', ast.unparse(node.test))
                true_state = f"{current}_T"
                false_state = f"{current}_F"
                diagram.append(f"state {true_state}")
                diagram.append(f"state {false_state}")
                diagram.append(f"{current} --> {true_state}: {cond}")
                diagram.append(f"{current} --> {false_state}: not {cond}")
                for stmt in node.body:
                    walk(stmt, true_state)
                for stmt in node.orelse:
                    walk(stmt, false_state)

        for node in tree.body:
            walk(node, "Start")
        diagram.append("Start --> [*]")
        return "\n".join(diagram)
    except Exception as e:
        return f"%% Error parsing Python code: {str(e)}"


def generate_class_diagram_python(code: str) -> str:
    try:
        tree = ast.parse(code)
        diagram = ["classDiagram"]
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                diagram.append(f"class {node.name} {{")
                for stmt in node.body:
                    if isinstance(stmt, ast.FunctionDef):
                        args = [a.arg for a in stmt.args.args if a.arg != "self"]
                        diagram.append(f"  +{stmt.name}({', '.join(args)})")
                    elif isinstance(stmt, ast.Assign):
                        for t in stmt.targets:
                            if isinstance(t, ast.Name):
                                diagram.append(f"  +{t.id}")
                diagram.append("}")
        return "\n".join(diagram)
    except Exception as e:
        return f"%% Error parsing Python code: {str(e)}"


# -------------------------
# JAVA/C DIAGRAMS (no changes)
# -------------------------
def parse_java_c(code: str) -> dict:
    functions = re.findall(r"(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\((.*?)\)\s*\{", code)
    classes = re.findall(r"class\s+(\w+)", code)
    return {"functions": functions, "classes": classes}


def generate_flowchart_java_c(parsed: dict) -> str:
    diagram = ["flowchart TD", "Start([Start])"]
    last_node = "Start"
    for func, _ in parsed["functions"]:
        func_node = f"N{func}"
        diagram.append(f"{last_node} --> {func_node}")
        last_node = func_node
    diagram.append(f"{last_node} --> End([End])")
    return "\n".join(diagram)


def generate_sequence_java_c(parsed: dict) -> str:
    diagram = ["sequenceDiagram"]
    for func, _ in parsed["functions"]:
        diagram.append(f"participant {func}")
    return "\n".join(diagram)


def generate_state_machine_java_c(parsed: dict) -> str:
    diagram = ["stateDiagram-v2", "[*] --> Start"]
    for func, _ in parsed["functions"]:
        diagram.append(f"Start --> {func}: enter {func}")
        diagram.append(f"{func} --> [*]")
    return "\n".join(diagram)


def generate_class_diagram_java_c(parsed: dict) -> str:
    diagram = ["classDiagram"]
    for cls in parsed["classes"]:
        diagram.append(f"class {cls} {{}}")
    return "\n".join(diagram)
