import nextcord
from nextcord.ext import commands
import random

class tictactoe(commands.Cog):
  def __init__(self, bot):
        self.bot = bot
 

  @commands.command()
  async def startXO(self, ctx, *,  target : nextcord.Member=None):
    """ Start a tic tac toe game with a mentioned user. """
    if not ctx.message.mentions:
      await ctx.send("You have to mention someone else in order to play... or do u want to play by yourself?\nhttps://tenor.com/9yK4.gif")
    
    elif target.name==ctx.author.name:
      await ctx.send("You have to mention someone else in order to play... or do u want to play by yourself?\nhttps://tenor.com/9yK4.gif")

    elif str(target.id)=='842228270400536586':
      await ctx.send("Hehe... u seriously mentioned me? It seems u don't have friends!\nhttps://tenor.com/QC0C.gif")
    
    else:
      board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
      state=1
      end=0
      move=0
      choice=0
      counter=0
      turn='X'
      player=1
      p1=ctx.author
      p2=target
      statement=""
      checkNum=['1','2','3','4','5','6','7','8','9']
      valid=False
      def printBoard(board):
        temp="```\n"
        for i in range(len(board)):
            temp += board[i]
            if i!=2 and i!=5 and i!=8:
                temp += "|"
            else:
                if i !=8:
                    temp+="\n-+-+-\n"
        temp+="\n```"
        return temp

      def checkState(board,counter, end, state, choice, turn, player):
        statement=""
        currentp=p1
        if player == '2':
          currentp=p2
        #check horizontally
        t=0
        for i in range(3):
          if board[t] == turn and board[t + 1] == turn and board[t + 2] == turn:
              statement=currentp.mention + " has won\nGAME OVER\n"
              end = 1
              break
          t += 3
      
        #check vertically
        t = 0;
        for i in range(3):
          if board[t] == turn and board[t + 3] == turn and board[t + 6] == turn:
              statement=currentp.mention + " has won\nGAME OVER\n"
              end = 1
              break
          t = i+1

        #check RDiagonal
        t = 0;
        if board[t] == turn and board[t + 4] == turn and board[t + 8] == turn:
            statement=currentp.mention + " has won\nGAME OVER\n"
            end = 1

        #check LDiagonal
        t = 2;
        if board[t] == turn and board[t + 2] == turn and board[t + 4] == turn:
          statement=currentp.mention + " has won\nGAME OVER\n"
          end = 1

        #check if tie
        if counter == 8 and end==0:
          statement="\nIt's a TIE!\nGAME OVER\n"
          end = 1

        if end == 1:
          state=0

        return board,statement,end,counter,choice,state,turn
      
      while state==1:
        if counter==0:
          player=random.randint(1,2)
          player=str(player)
          await ctx.send(printBoard(board))

          currentp=p1
          if player == '2':
            currentp=p2
          #choose X or O
          
          await ctx.send(currentp.mention + ", Do u want to be X or O?(0/1)")
          while not valid:
            def check(m):
              return m.author.name == currentp.name and m.channel == ctx.channel
            response = await self.bot.wait_for('message', check=check)
            if response.content == "0" or response.content == "1":
              valid=True
              choice=int(response.content)
              if choice==0:
                  turn='X'
              else:
                  turn='O'

          valid=False

        while move==0:
          await ctx.send(currentp.mention + " choose where to put the " + turn + "(1-9): ")
          
          while not valid:
            def check(m):
              return m.author.name == currentp.name

            response = await self.bot.wait_for('message', check=check)
            for x in checkNum:
              if response.content==x:
                valid=True
                break
            if valid:
              choice=int(response.content)
              choice-=1
              if board[choice] == ' ':
                board[choice] = turn
                move = 1
              else:
                await ctx.send("This slot is already taken")
              
        valid=False
        move=0
        
        await ctx.send(printBoard(board))

        board,statement,end,counter,choice,state,turn=checkState(board, counter, end, state, choice, turn, player)
        if statement:
          await ctx.send(statement)

        if state==0:
            break

        #switch turn
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'

        if player == '1':
            player = '2'
            currentp=p2
        else:
            player = '1'
            currentp=p1
        
        counter+=1
    


def setup(bot):
  bot.add_cog(tictactoe(bot))