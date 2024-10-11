import pydot
import os
import toml

os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz-12.1.2-win64\\bin\\'

def makeDependencyList(name):
    listDeps = [{}]
    with open(name, 'r') as apkindex:
        index = 0;
        for line in apkindex:
            if(line == "" or line == "\n"):
                listDeps.append({})
                index += 1
            else:
                if line.startswith("P:"):
                    listDeps[index].update({"name": line[2:-1]})
                elif line.startswith("p:"):
                    things = list(line[2:-1].split(" "))
                    for i in range(len(things)):
                        ind = things[i].find("=")
                        things[i] = things[i][:ind]
                    listDeps[index].update({"provides": things})
                elif line.startswith("D:"):
                    listDeps[index].update({"depends": list(line[2:-1].split(" "))})

            if "provides" not in listDeps[index]:
                listDeps[index].update({"provides": []})
            if "depends" not in listDeps[index]:
                listDeps[index].update({"depends": []})
    return listDeps[:-1]

def generateDot(map):
    graph_lines = ["digraph dependencies {"]
    for dep in map.keys():
        subdeps = map[dep]
        for subdep in subdeps:
            graph_lines.append(f'"{dep}" -> "{subdep}";')
    graph_lines.append("}")
    lines = "\n".join(graph_lines)
    with open("graph.dot", "wb") as dot_file:
        dot_file.write(lines.encode())
        dot_file.close()

def visualizeGraph():
    graphs = pydot.graph_from_dot_file("graph.dot")
    graph = graphs[0]
    graph.write_png("res.png")


def findPacket2(listt, name, res):
    pack = [x for x in listt if x["name"] == name]
    if len(pack) > 0:
        pack = pack[0]
    else:
        pack = {"name": "", "depends": []}
    n = pack["name"]
    d = pack["depends"]
    nextdeps = []
    for dep in d:
        p = [x["name"] for x in listt if dep in x["provides"]]
        if len(p) > 0:
            nextdeps.append(p[0])
        else:
            nextdeps.append(dep)
    res[n] = nextdeps
    for dep in d:
        if dep.startswith("so:"):
            provPacket = [x for x in listt if dep in x["provides"]][0]
            findPacket2(listt, provPacket["name"], res)
        else:
            findPacket2(listt, dep, res)


if __name__ == "__main__":
    with open('instructions.toml', 'r') as f:
        config = toml.load(f)

    package = config["packagename"]

    listDeps = makeDependencyList("APKINDEX")

    res = {}
    findPacket2(listDeps, package, res)
    print(res)

    generateDot(res)
    visualizeGraph()
