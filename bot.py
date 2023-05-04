from discord.ext import commands, tasks
import discord
import uuid
import os
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Declare a global variable to store the state of the task
task_status = "stopped"
import asyncio


@tasks.loop(minutes=60)
async def send_used_keys():
  # Check if the task is currently running
  if task_status == "running":
    # Create a File object for the used keys file
    used_keys_file = discord.File("used keys.txt")

    # Send the used keys file to the specified channel
    channel = bot.get_channel(1052565208138272858)
    await channel.send(file=used_keys_file)

    # Sleep for 2 minutes before sending the file again
    await asyncio.sleep(3600)


@bot.event
async def on_ready():
  print("Bot is online and ready")


@bot.command()
async def start(ctx):
  global task_status

  # Set the task status to "running"
  task_status = "running"

  # Start the task
  send_used_keys.start()

  # Confirm that the task has been started
  await ctx.send("Task started successfully")


@bot.command()
async def stop(ctx):
  global task_status

  # Set the task status to "stopped"
  task_status = "stopped"
  send_used_keys.stop()
  # Confirm that the task has been stopped
  await ctx.send("Task stopped successfully")


@bot.command()
async def gen(ctx, key_length, amount, service):
  # Check if the required arguments have been provided
  if key_length is None or amount is None or service is None:
    em = discord.Embed(color=0xff0000)
    error_message = "Error: "
    if key_length is None:
      error_message += "Please provide the key length in your command. "
    if amount is None:
      error_message += "Please provide the amount of keys to generate in your command. "
    if service is None:
      error_message += "Please provide the service for which to generate keys in your command. "
    em.add_field(name="Error", value=error_message)
    await ctx.send(embed=em)
    return 0

  # Check if the user is an administrator
  if not ctx.message.author.guild_permissions.administrator:
    em = discord.Embed(color=0xff0000)
    em.add_field(name="Error",
                 value="Only administrators can use this command!")
    await ctx.send(embed=em)
    return 0

  # Generate the keys (rest of the code remains unchanged)
  key_amt = range(int(amount))
  f = open("keys.txt", "a")
  show_key = ''
  for x in key_amt:
    # Generate a key with the specified length
    key = str(uuid.uuid4())[:int(key_length)]
    show_key += "\n" + key
    f.write(key + ":" + service)  # Include the service in the generated keys
    f.write("\n")

  if len(str(show_key)) == 37:
    show_key = show_key.replace('\n', '')
    await ctx.send(f"Key for {service}: {show_key}"
                   )  # Include the service in the message
    return 0
  if len(str(show_key)) > 37:
    await ctx.send(f"Keys for {service}: {show_key}"
                   )  # Include the service in the message
  else:
    await ctx.send("Somthings wrong")


@bot.command()
async def redeem(ctx, key):
  # Check if a key has been provided
  if key is None or key == "":
    em = discord.Embed(color=0xff0000)
    em.add_field(
      name="Error",
      value="Please provide a key to redeem after the .redeem command.")
    await ctx.send(embed=em)
    return 0

  # Look for the key in the "keys.txt" file
  with open("keys.txt") as f:
    for line in f:
      parts = line.split(":")
      if parts[0] == key:
        # Key is valid, check if it has already been used
        with open("used keys.txt") as used_f:
          if key in used_f.read():
            em = discord.Embed(color=0xff0000)
            em.add_field(
              name="Invalid Key",
              value="Inputed key has already been used for the {} service!".
              format(parts[1]))
            await ctx.send(embed=em)
            return 0
          else:
            # Key is valid and has not been used, redeem it
            em = discord.Embed(color=0x008525)
            em.add_field(
              name="Key Redeemed",
              value=f"Key has now been redeemed for the {parts[1]} service")
            await ctx.send(embed=em)

            # Check if the service is Netflix and ping a channel
            if parts[1] == "netflix-basic" or parts[1] == "netflix-premium":

              channel = bot.get_channel(1048174572412866570)
              await channel.send(
                "A key for Netflix has been redeemed, check out our suggestions!"
              )

            f = open("used keys.txt", "a")
            f.write(key)
            f.write('\n')
            return 0

    else:
      # Key is not valid
      em = discord.Embed(color=0xff0000)
      em.add_field(name="Invalid Key",
                   value="Inputed key is not valid for any service!")
      await ctx.send(embed=em)


bot.run("MTA5ODI5MzI3NTc3OTE1ODE4Ng.Gk8LWQ.7DGoxpH_KaOs9Cx1E-QnzgGGD7YlObNvljdRgo")