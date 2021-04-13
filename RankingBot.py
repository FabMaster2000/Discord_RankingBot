import discord
import sqlite3
import asyncio

class MyClient(discord.Client):
    #Einloggen
    async def on_ready(self):
        #print("Bin da :)")
        conn = sqlite3.connect("rankingbot.db")
        cursor = conn.cursor()

    #Nachricht lesen
    async def on_message(self, ctx):
        def crimeSwitcher(argument):
            switcher = {
                "Kontrolle": 1,
                "Blitzerfoto": 5,
                "Mängelbescheid": 10,
                "Fahrverbot": 20,
                "Stilllegung": 30,
                "MPU": 50
            }
            return switcher.get(argument, "No Crime found")

        channel = ctx.channel
        conn =sqlite3.connect('rankingbot.db')
        conn.execute('create table if not exists points(id integer AUTO_INCREMENT primary key, points_name text, points integer)')
        cursor = conn.cursor()
        if ctx.author == client.user:
            return

        if ctx.content == "?users":
            cursor.execute("select * from points")
            table = cursor.fetchall()
            usersString = ""
            i = 0
            for user in table:
                username = table[i][1]
                point = table[i][2]
                usersString+= username + " with " + str(point) + " points\n\n"
                i+=1
            await channel.send(embed = discord.Embed(title="Current userlist:", description=usersString))
            

        if ctx.content == "?stats":
            cursor.execute("select points_name, points from points where points = (select max(points) from points)")
            max_pointsObject = cursor.fetchone()
            await channel.send("The higeste Score has " + max_pointsObject[0] + " with " + str(max_pointsObject[1]) + " points. Congrats!!")

        if ctx.content == "?add":
            await channel.send(embed=discord.Embed(title="Please type the username you will add Points", description="Timout error is set to 10 sek."))
            try:
                bot_input = await self.wait_for(
                    "message",
                    timeout=10,
                    check=lambda  message: message.author == ctx.author and message.channel == channel
                )
                input_username = bot_input.content
                cursor.execute("select * from points")
                table = cursor.fetchall()
                i = 0
                created = True
                for user in table:
                    if input_username != table[i][1]:
                        created = False
                    else:
                        created = True
                        break
                    #print(table[i][1])
                    i+=1
                if created == False and input_username != "cancel":
                    await channel.send(embed=discord.Embed(title="User is not registered!"))
                if input_username == "cancel":
                    await channel.send(embed=discord.Embed(title="Canceled!"))
                else:
                    await channel.send(embed=discord.Embed(
                        title="Type the crime",
                        description="Timout error is set to 10 sek.\n\n"
                                    "Kontrolle\n"
                                    "Blitzerfoto\n"
                                    "Mängelbescheid\n"
                                    "Fahrverbot\n"
                                    "Stilllegung\n"
                                    "MPU"
                    ))
                    try:
                        bot_input = await self.wait_for(
                            "message",
                            timeout=10,
                            check=lambda  message: message.author == ctx.author and message.channel == channel)
                        crime = crimeSwitcher(bot_input.content)
                        if isinstance(crime, int):
                            cursor.execute('update points set points = points + (?) where points_name = (?)', (crime, input_username))
                            conn.commit()
                            await channel.send(embed=discord.Embed(title="Score of " + input_username + " is updated."))
                        else:
                            await channel.send(embed=discord.Embed(title=crime))

                    except asyncio.TimeoutError:
                        await channel.send(embed=discord.Embed(title="Timout error!"))

            except asyncio.TimeoutError:
                await channel.send(embed=discord.Embed(title="Timout error!"))


        if ctx.content == "?create" :
            await channel.send(embed=discord.Embed(title="Please type the username you will create", description="Timout error is set to 10 sek."))

            try:
                
                bot_input = await self.wait_for(
                    "message",
                    timeout=10,
                    check=lambda  message: message.author == ctx.author and message.channel == channel
                )

                input_username = bot_input.content

                cursor.execute("select * from points")
                table = cursor.fetchall()
                i = 0
                create = True
                for user in table:
                    if input_username == table[i][1]:
                        
                        create = False
                        await channel.send(embed=discord.Embed(title="User is already registered!"))
                    i+=1

                if input_username == "cancel":
                    await channel.send(embed=discord.Embed(title="Canceled!"))
                    
                if create:
                    conn.execute('insert into points (points_name, points) values (?,?)', (input_username, 0))
                    conn.commit()
                    await channel.send(embed=discord.Embed(title="User '" + input_username + "' is created."))
                    
            except asyncio.TimeoutError:
                await channel.send(embed=discord.Embed(title="Timout error!"))
        conn.close()

        if ctx.content == "?pointlist":
            await channel.send(embed=discord.Embed(
                title="Ranking-Bot Command help:",
                description="Kontrolle mit Beweisfoto : 1 Punkt"
                            "\n\nBlitzerfoto : 5 Punkte"
                            "\n\nMängelbescheid : 10 Punkte "
                            "\n\nFahrverbot pro Monat : 20 Punkte "
                            "\n\nStilllegung : 30 Punkte"
                            "\n\nMPU : 50 Punkte"
            ))

        if ctx.content == "?remove":
            conn = sqlite3.connect("rankingbot.db")
            cursor = conn.cursor()
            await channel.send(embed=discord.Embed(
                title="Type the user where you will remove points"))

            try:
                bot_input = await self.wait_for(
                    "message",
                    timeout=10,
                    check=lambda  message: message.author == ctx.author and message.channel == channel
                )
                input_username = bot_input.content
                cursor.execute("select * from points")
                table = cursor.fetchall()
                i = 0
                created = True
                for user in table:
                    if input_username != table[i][1]:
                        created = False
                    else:
                        created = True
                        break
                    #print(table[i][1])
                    i+=1
                if created == False and input_username != "cancel":
                    await channel.send(embed=discord.Embed(title="User is not registered!"))
                if input_username == "cancel":
                    await channel.send(embed=discord.Embed(title="Canceled!"))
                else:
                    await channel.send(embed=discord.Embed(
                        title="Type the points you will remove",
                        description="Timout error is set to 10 sek."))
                    try:
                        bot_input = await self.wait_for(
                            "message",
                            timeout=10,
                            check=lambda  message: message.author == ctx.author and message.channel == channel)
                        points = int(bot_input.content)
                        if isinstance(points, int):
                            cursor.execute('update points set points = points - (?) where points_name = (?)', (points, input_username))
                            conn.commit()
                            await channel.send(embed=discord.Embed(title="Score of " + input_username + " is updated."))
                        else:
                            await channel.send(embed=discord.Embed(title=crime))

                    except asyncio.TimeoutError:
                        await channel.send(embed=discord.Embed(title="Timout error!"))

            except asyncio.TimeoutError:
                await channel.send(embed=discord.Embed(title="Timout error!"))
            

        if ctx.content == "?":
            await channel.send(embed=discord.Embed(
                title="Ranking-Bot Command help:",
                description="? : help "
                            "\n\n?create : create a new User "
                            "\n\n?users : print all users "
                            "\n\n?stats : show the current stats "
                            "\n\n?pointlist : show the points which you could get"
                            "\n\n?add : to add points"
            ))



client = MyClient()

#discord Bot id
client.run("$discordbotid")