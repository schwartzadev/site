# coding=utf-8
from flask import redirect

from pysite.base_route import RouteView


class InviteView(RouteView):
    path = "/invite"
    name = "invite"

    def get(self):
        return redirect("https://discord.gg/8NWhsvT")
