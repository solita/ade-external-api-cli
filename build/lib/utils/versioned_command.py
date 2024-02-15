import click
import re

class VersionedCommand(click.Command):

    def format_usage(self, ctx, formatter):
            rv = ""
            if ctx.info_name is not None:
                rv = re.sub('\d?(-v\d{1})$', '', ctx.info_name)
            if ctx.parent is not None:
                parent_command_path = [ctx.parent.command_path]

            version = re.search('(?<=-v)(\d{1})$', ctx.info_name).group(1)
            command_path = f"{' '.join(parent_command_path)} --version {version} {rv}"
            pieces = self.collect_usage_pieces(ctx)
            formatter.write_usage(command_path, " ".join(pieces))