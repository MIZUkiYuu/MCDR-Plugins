from mcdreforged.api.all import *

OVERWORLD = "overworld"
NETHER = "the_nether"
END = "the_end"

PREFIX_DIM = "!!dim"
PREFIX_OVERWORLD = "!!overworld"
PREFIX_NETHER = "!!nether"
PREFIX_END = "!!end"


def show_help(source):
    source.reply(
        """
§7!!overworld §r在地狱，传送到主世界对应坐标（地狱坐标*8）,在末地，传送至当前坐标
§7!!overworld <x> <y> <z> §r传送到主世界指定坐标
§7!!nether §r在主世界，传送到地狱对应坐标（主世界坐标/8）,在末地，传送至当前坐标
§7!!nether <x> <y> <z> §r传送到地狱指定坐标
§7!!end §r传送到末地祭坛上空(0,100,0)
§7!!end <x> <y> <z> §r传送到末地指定坐标
"""
    )


@new_thread("TpDimension")
def teleport_dimension_here(source: CommandSource, target_dim):
    api = source.get_server().get_plugin_instance("minecraft_data_api")
    pos = api.get_player_coordinate(source.player)
    dim = api.get_player_dimension(source.player)
    teleport_dimension(source, pos.x, pos.y, pos.z, dim, target_dim)


def teleport_dimension(source: CommandSource, x, y, z, loc_dim, target_dim):
    if target_dim == 0:
        if loc_dim == -1:
            teleport(source, x * 8, y, z * 8, OVERWORLD)
        elif loc_dim == 1:
            teleport(source, x, y, z, OVERWORLD)
    elif target_dim == -1:
        if loc_dim == 0:
            teleport(source, x / 8, y, z / 8, NETHER)
        elif loc_dim == 1:
            teleport(source, x, y, z, NETHER)
    elif target_dim == 1:
        teleport(source, 0, 100, 0, END)
    else:
        teleport(source, x, y, z, target_dim)


def teleport(source: CommandSource, x, y, z, target_dim):
    source.get_server().execute(
        "execute in {} run tp {} {} {} {}".format(target_dim, source.player, x, y, z)
    )


def on_load(server, info):
    server.register_help_message("!!dim", "查看如何快速传送到指定维度")
    server.register_command(Literal(PREFIX_DIM).runs(show_help))
    server.register_command(
        Literal(PREFIX_OVERWORLD)
        .runs(lambda src: teleport_dimension_here(src, 0))
        .then(
            Number("x").then(
                Number("y").then(
                    Number("z").runs(
                        lambda src, ctx: teleport(
                            src, ctx["x"], ctx["y"], ctx["z"], OVERWORLD
                        )
                    )
                )
            )
        )
    )
    server.register_command(
        Literal(PREFIX_NETHER)
        .runs(lambda src: teleport_dimension_here(src, -1))
        .then(
            Number("x").then(
                Number("y").then(
                    Number("z").runs(
                        lambda src, ctx: teleport(
                            src, ctx["x"], ctx["y"], ctx["z"], NETHER
                        )
                    )
                )
            )
        )
    )
    server.register_command(
        Literal(PREFIX_END)
        .runs(lambda src: teleport_dimension_here(src, 1))
        .then(
            Number("x").then(
                Number("y").then(
                    Number("z").runs(
                        lambda src, ctx: teleport(
                            src, ctx["x"], ctx["y"], ctx["z"], END
                        )
                    )
                )
            )
        )
    )
