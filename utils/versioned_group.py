import click
import re

class VersionedGroup(click.Group):

    def resolve_command(self, ctx, args):
        # always return the full command name

        version = ctx.params['version']
        args[0] = f'{args[0]}-v{version}'


        _, cmd, args = super().resolve_command(ctx, args)

        return cmd.name, cmd, args

    def command(self, *args, **kwargs):
        """Gather the command help groups"""
        help_group = kwargs.pop('group', None)

        decorator = super(VersionedGroup, self).command(*args, **kwargs)

        def wrapper(f):
            cmd = decorator(f)
            cmd.help_group = help_group
            return cmd

        return wrapper

    def format_commands(self, ctx, formatter):
        # Modified fom the base class method

        for param in self.params:
            if param.name == "version":
                default_version = param.default

        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if not (cmd is None or cmd.hidden):
                commands.append((subcommand, cmd))

        if commands:
            longest = max(len(cmd[0]) for cmd in commands)
            # allow for 3 times the default spacing
            limit = formatter.width - 6 - longest

            groups = {}
            for subcommand, cmd in commands:

                subcommand = re.sub('\d?(-v\d{1})$', '', subcommand)
                help_str = cmd.get_short_help_str(limit)
                subcommand += ' ' * (longest - len(subcommand))
                groups.setdefault(
                    cmd.help_group, []).append((subcommand, help_str))

            with formatter.section('Commands'):
                for group_name, rows in sorted(groups.items()):
                    regexp = re.compile(f'.*V{default_version}.*')
                    if regexp.search(group_name):
                        group_name += " (default)"
                    with formatter.section(group_name):
                        formatter.write_dl(rows)