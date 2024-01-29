from infini.loader import Loader
from infini.input import Input
from ipm import api
from ipm.models.ipk import InfiniProject
from pathlib import Path

ipk = InfiniProject(Path(__file__).resolve().parent)
api.build(Path(__file__).resolve().parent, echo=True)
api.install(
    str(Path(__file__).resolve().parent.joinpath("dist", f"{ipk.default_name}")),
    force=True,
    upgrade=True,
    echo=True,
)

with Loader() as loader:
    loader.load(ipk.name)
    core = loader.into_core()

commands = [
    ".r20#d6",
    "ti",
    "li",
    ".sc 1d10/1d10",
    ".coc cache",
    ".coc 200",
    ".coc set 2",
    ".coc 2 name 苏向夜",
    ".coc cache",
    ".coc set 1",
    ".ra",
    ".ra 毁灭人类"
]


def test():
    for command in commands:
        print("测试指令:", command)
        print("=============== start ===============")
        for output in core.input(Input(command)):
            print(output)
        print("================ end ================")
        print()


test()
