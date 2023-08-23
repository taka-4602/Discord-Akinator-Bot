import discord
from akinator import (
    CantGoBackAnyFurther,
    InvalidAnswer,
    AsyncAkinator,
    Answer,
    Theme,
    Language
)

intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = discord.app_commands.CommandTree(client)

BOTTOKEN="Botのトークンをここに"

@client.event
async def on_ready():
    print(f'Akinator is running! {client.user}')
    await tree.sync()

class akiview(discord.ui.View):
            
            def __init__(self, timeout=180,):
                super().__init__(timeout=timeout)
                self.value=None

            
            @discord.ui.button(label="はい", style=discord.ButtonStyle.primary,custom_id="1")
            async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 1
                self.stop()

            @discord.ui.button(label="いいえ", style=discord.ButtonStyle.danger,custom_id="2")
            async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 2
                self.stop()         

            @discord.ui.button(label="わからない", style=discord.ButtonStyle.secondary,custom_id="3")
            async def idk(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 3
                self.stop()
            @discord.ui.button(label="たぶんそう", style=discord.ButtonStyle.success,custom_id="4")
            async def maybe(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 4
                self.stop()

            @discord.ui.button(label="たぶん違う", style=discord.ButtonStyle.danger,custom_id="5")
            async def maybeno(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 5
                self.stop()
            
            @discord.ui.button(label="⬅️1つもどる", style=discord.ButtonStyle.primary,custom_id="6")
            async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 6
                self.stop()

            @discord.ui.button(label="⛔やめる", style=discord.ButtonStyle.primary,custom_id="7")
            async def quit(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 7
                self.stop()


class winview(discord.ui.View):
            
            def __init__(self, timeout=15,):
                super().__init__(timeout=timeout)
                self.value=None
           
            
            @discord.ui.button(label="あってる", style=discord.ButtonStyle.primary,custom_id="1")
            async def correct(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 1
                self.stop()

            @discord.ui.button(label="ちがう", style=discord.ButtonStyle.danger,custom_id="2")
            async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 2
                self.stop()         

            @discord.ui.button(label="もういっかい最初から！", style=discord.ButtonStyle.secondary,custom_id="3")
            async def res(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.value = 3
                self.stop()


@tree.command(name='akinator', description='Akinatorを開始')
async def aki_sta(interaction: discord.Interaction,英語:bool=False,動物:bool=False):
  if 英語==True:
      if 動物==True:
          lan="English"
          the="animals"
      else:
          lan="English"
          the="characters"
  else:
      if 動物==True:
          lan="Japanese"
          the="animals"
      else:
          lan="Japanese"
          the="characters"
  await interaction.response.send_message('Akinatorを開始...')
  aki = AsyncAkinator(
            child_mode=False,
            language=Language.from_str(lan),
            theme=Theme.from_str(the),
        )
  try:
            first_question = await aki.start_game()
  except:
            msg = await interaction.original_response()
            await msg.edit(content='Akinatorを開始...できなかった.....')
            return
  a=2
  view = akiview()
  msg = await interaction.original_response()
  ques= await msg.edit(content=None,view=view,embed = discord.Embed(title=(f'質問 1\n**{first_question}**'),description=("***ここが先頭***"),color=discord.Colour.yellow()))
  maeq=first_question
  await view.wait()
  if view.value==1:
                answer="y"
                maes="はい"
  elif view.value==2:
                answer="n"
                maes="いいえ"
  elif view.value==3:
                answer="idk"
                maes="わからない"
  elif view.value==4:
                answer="p"
                maes="たぶんそう"
  elif view.value==5:
                answer="pn"
                maes="たぶん違う"
  elif view.value==6:
                answer="back"
                maes="1つもどる" 
  elif view.value==7:
                await msg.edit(content="おしまい",view=None,embed = None)
                return   
             
  while aki.progression <= 99:
            try:
                if answer == 'back':
                    try:
                        await aki.back()
                        a=a-2
                    except CantGoBackAnyFurther:
                        maeq='これが最初の質問です'
                        a=a-1
                        maes="🕊️"
                else:
                    try:
                        answer = Answer.from_str(answer)
                    except InvalidAnswer:
                        await interaction.channel.send('あ')
                    else:
                        try:
                            await aki.answer(answer)
                        except:
                            await msg.edit(content="Akinatorから応答がないのでゲームが終了しました...",view=None,embed = None)
                            break
                            
            except:
                await msg.edit(content='タイムアウト',view=None,embed = None)                               
                break                       
            view = akiview()
            await ques.edit(view=view,embed = discord.Embed(title=(f'質問 {a}\n**{aki.question}**'),description=(f"前の選択\n{maeq} / {maes}"), color=discord.Colour.yellow()))
            a=a+1           
            maeq=aki.question                
            await view.wait()
            if view.value==1:
                    answer="y"
                    maes="はい"
            elif view.value==2:
                    answer="n"
                    maes="いいえ"
            elif view.value==3:
                    answer="idk"
                    maes="わからない"
            elif view.value==4:
                    answer="p"
                    maes="たぶんそう"
            elif view.value==5:
                    answer="pn"
                    maes="たぶん違う"
            elif view.value==6:
                    answer="back"
                    maes="1つもどる"
            elif view.value==7:
                await msg.edit(content="おしまい",view=None,embed = None)
                break
            
            if aki.progression >= 80:
                first_guess = await aki.win()
                view = winview()
            
                if first_guess:
                    emb = discord.Embed(title=(first_guess.name),description=(first_guess.description)+"\n\nランキング : **#"+(first_guess.ranking)+"**", color=discord.Colour.blue())
                    emb.set_image(url=first_guess.absolute_picture_path)
                    await ques.edit(view=view,embed=emb)
                    await view.wait()
                    if view.value==1:
                            emb = discord.Embed(title="**"+(first_guess.name)+"**",description=(first_guess.description)+"\n\nランキング : **#"+(first_guess.ranking)+"**", color=discord.Colour.blue())
                            emb.set_image(url=first_guess.absolute_picture_path)
                            await ques.edit(view=None,embed=emb)
                            break
                    elif view.value==2:
                            if aki.progression >= 96:
                                await ques.edit(view=None,content=None,embed = discord.Embed(title="キャラクターまでたどり着きませんでした...",color=discord.Colour.green()))
                                break
                            await ques.edit(view=None,content=None,embed=discord.Embed(title="質問を再開...",color=discord.Colour.purple()))
                            continue
                    elif view.value==3:
                            await ques.edit(view=None,embed = discord.Embed(title="最初から開始",color=discord.Colour.purple()))
                            while a>0:
                                try:
                                    await aki.back()
                                    a=a-1
                                except CantGoBackAnyFurther:
                                    break
                            a=2
                            view = akiview()
                            await ques.edit(view=view,content=None,embed = discord.Embed(title=(f'質問 1\n**{first_question}**'),description=("***ここが先頭***"),color=discord.Colour.yellow()))
                            maeq=first_question
                            await view.wait()
                            if view.value==1:
                                    answer="y"
                                    maes="はい"
                                    continue
                            elif view.value==2:
                                    answer="n"
                                    maes="いいえ"
                                    continue
                            elif view.value==3:
                                    answer="idk"
                                    maes="しらん"
                                    continue
                            elif view.value==4:
                                    answer="p"
                                    maes="たぶん"
                                    continue
                            elif view.value==5:
                                    answer="pn"
                                    maes="たぶん違う"
                                    continue
                                    
                            elif view.value==6:
                                    answer="back"
                                    maes="1つもどる" 
                                    continue
                            elif view.value==7:
                                await msg.edit(content="おしまい",view=None,embed = None)
                                break
                    else:
                            emb = discord.Embed(title="**"+(first_guess.name)+"**",description=(first_guess.description)+"\n\nランキング : **#"+(first_guess.ranking)+"**", color=discord.Colour.blue())
                            emb.set_image(url=first_guess.absolute_picture_path)
                            await ques.edit(view=None,embed=emb)
                            break
            if a==80:
                await ques.edit(view=None,content=None,embed = discord.Embed(title="80かいめまでにあてられなかったのでAkinatorの負け！",color=discord.Colour.green()))
                break


client.run(BOTTOKEN)