#built in
from sys import argv
from os import path, chdir, mkdir
#self
from eb_files import ui, data, core

def offset(list):
    for i in range(0, len(list)):
        if i > 0:
            list[i] -= i
    return list

def inputs():
    while True:
        nums = better.input('Select the bots you wish to select by listing the number corrosponding (e.g. 1 2 4): ').split(' ')
        try:
            nums = sorted(list(map(int, nums)))
            break
        except ValueError as e:
            print(e)
    return nums

class better:
    input_called = -1
    try:
        input_commands = [c.replace('\n', '') for c in open(argv[1], 'r').readlines() if not c.startswith('#')]
    except:
        input_commands = []
    def input(*string):
        if string:
            print(string[0], end='')
        better.input_called += 1
        try:
            print(better.input_commands[better.input_called], end='')
            return better.input_commands[better.input_called]
        except:
            return input()
class commands:
    def help():
        ui.sys_message('Commands List')
        ui.list_dict(choices)
    def add():
        tks = better.input('What is your bot token(s) (if multiple, seperate them with spaces)? Obtain it from https://discord.com/developers/ and paste it here: ').split(' ')
        exist_tks = data.extract_tks()
        for tk in tks:
            if not tk in exist_tks:
                data.save(tk, better.input(f'Prefix for {tk}: '))
            else:
                print(tk, 'already exists in the database; Please remove the previous entry before trying to add this token again')
        ui.sys_message('Success')
    def rm():
        bot = data.extract()
        ui.num_list(bot)
        if bot != []:
            bot_rm_nums = inputs()
            for bot_rm_num in offset(bot_rm_nums):
                data.remove(bot_rm_num)
            ui.sys_message('Success')
        else:
            ui.sys_message('There are no bots stored')
    def boota():
        bots = data.extract()
        if bots != []:
            for bot in bots:
                core.boot(bot)
        else:
            ui.sys_message('There are no bots stored')
    def boots():
        bots = data.extract()
        ui.num_list(bots)
        if bots != []:
            bot_stp_nums = inputs()
            for bot_st_num in bot_stp_nums:
                core.boot(bots[bot_st_num])
        else:
            ui.sys_message('There are no bots stored')
    def boott():
        tk = better.input('What is the bot token?\n')
        px = better.input('What is the desired bot prefix?\n')
        bot = dict(token = tk, prefix = px)
        core.boot(bot)
    def install():
        from wget import download
        while True:
            link = input("Link: ")
            if link.endswith('.py'):
                download(f'{link}', f'{path.dirname(path.abspath(__file__))}/cogs')
                break
    def running():
        ui.sys_message("Currently active")
        ui.num_list(core.processes)
    def restart():
        core.list_threads()
        if core.processes != []:
            bot_stp_nums = inputs()
            for bot_stp_num in offset(bot_stp_nums):
                bot = core.processes[bot_stp_num]
                core.stop(bot_stp_num)
                core.boot(dict(token = bot[0], prefix = bot[1]))
            ui.sys_message('Successfully restarted the bots')
        else:
            ui.sys_message('There are no bots running')
    def kill():
        core.list_threads()
        if core.processes != []:
            bot_stp_nums = inputs()
            for bot_stp_num in offset(bot_stp_nums):
                core.stop(bot_stp_num)
            ui.sys_message('Successfully stopped the bots')
        else:
            ui.sys_message('There are no bots running')
    def quit():
        if core.processes != []:
            for bots in range(0, len(core.processes)):
                core.stop(0)
        quit()
if __name__ == '__main__':
    chdir(path.dirname(path.abspath(__file__)))
    try:
        mkdir('./data')
        open('./data/bots.easybot', 'w').close()
    except: pass
    try:
        mkdir('./cogs')
    except: pass
    choices = {
    'add': 'Add bot(s)',
    'rm': 'Remove bot(s)',
    'bootall':'Boot all',
    'bootspecific': 'Boot specific',
    'bootnotoken': 'Boot w/o saving token',
    'install': 'Installs cog from link',
    'kill': 'Stop Specific',
    'running': 'Shows running bots',
    'restart': 'Restart Specific',
    'quit': 'Quit'
    }
    i = 1
    ui.sys_message('EasyBot.py is running')
    while True:
        try:
            commands.help()
            ui.sys_message('Run your commands below')
            choice = better.input()
            ui.clear()
            if choice == 'add':
                commands.add()
            elif choice == 'rm':
                commands.rm()
            elif choice == 'bootall':
                commands.boota()
            elif choice == 'bootspecific':
                commands.boots()
            elif choice == 'bootnotoken':
                commands.boott()
            elif choice == 'install':
                commands.install()
            elif choice == 'running':
                commands.running()
            elif choice == 'restart':
                commands.restart()
            elif choice == 'kill':
                commands.kill()
            elif choice == 'quit':
                commands.quit()
            else:
                print(f"{choice} is not a proper command")
        except Exception as e:
            print(f'There has been an error: {e}')