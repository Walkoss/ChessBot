from chessbot.command import *

class CommandTakeback(Command):
    name = "takeback"
    aliases = ["undo"]
    help_string = "Request a takeback for a move"
    help_index = 120
    flags = FLAG_MUST_BE_IN_GAME

    @classmethod
    async def run(self,ctx):
        if len(ctx.game.moves) > 0:
            m = await ctx.ch.send("{u1}, {u2} is requesting a takeback!".format(u1=ment(ctx.game.players[not ctx.game.players.index(ctx.mem.id)]),u2=str(ctx.mem.mention)))
            await m.add_reaction(ACCEPT_MARK)
            await m.add_reaction(DENY_MARK)

            try:
                def check(reaction, user):
                    return user.id == ctx.game.players[not ctx.game.players.index(ctx.mem.id)] and str(reaction) in [ACCEPT_MARK, DENY_MARK]

                reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=10)

                if str(reaction) == ACCEPT_MARK:
                        ctx.game.pop("moves", 1)
                        ctx.game = db.Game.from_user_id(ctx.mem.id)
                        await ctx.ch.send(content= "The move has been taken back!", file=makeboard(ctx.game.board, orientation=ctx.game.board.turn))


                elif str(reaction) == DENY_MARK:
                    await ctx.ch.send("You have declined the takeback request!")

            except Exception as E:
                await ctx.ch.send("The takeback request has timed out!"+str(E))

        else:
            await ctx.ch.send(content= "There is no move to take back!")
