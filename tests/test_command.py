from infini.loader import Loader
from infini.input import Input
from ipm import api
from ipm.models.ipk import InfiniProject

import pytest


@pytest.fixture
def ipk() -> InfiniProject:
    return InfiniProject()


def test_install(ipk):
    api.build(ipk.source_path)
    api.install(
        str(ipk.source_path.joinpath("dist", f"{ipk.default_name}")),
        force=True,
        upgrade=True,
    )


def test_main(ipk):
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
        ".ra 毁灭人类",
    ]

    with Loader() as loader:
        loader.load(ipk.name)
        core = loader.into_core()

    for command in commands:
        print("测试指令:", command)
        print("=============== start ===============")
        for output in core.input(Input(command)):
            print(output)
        print("================ end ================")
        print()


if __name__ == "__main__":
    test_main(InfiniProject())
