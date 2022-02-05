from typing import re

from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission

from apibasics.models import Coach


class isAuthenticated(IsAuthenticated):
    """
    Grants access to authenticated users
    """

    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        return is_authenticated


class isRestricted(IsAuthenticated):
    """
    Grants access to non restricted critical operations
    """

    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)

        if is_authenticated:
            if request.method not in SAFE_METHODS:  # If request is something dangerous, check that the user is an admin
                has_permission = False
                return has_permission

            has_permission = True
            return has_permission

        else:
            has_permission = False
            return has_permission


class isPlayer(BasePermission):
    """
    Grants access to players
    """

    def has_permission(self, request, view):
        has_permission = request.user.groups.filter(name='player').exists()
        return has_permission


class isCoach(BasePermission):
    """
    Grants access to coaches
    """

    def has_permission(self, request, view):
        has_permission = request.user.groups.filter(name='coach').exists()
        return has_permission


class isAdmin(BasePermission):
    """
    Grants access to admin
    """

    def has_permission(self, request, view):
        has_permission = (request.user.groups.filter(name='admins').exists() | request.user.is_superuser)
        return has_permission


class isSameTeam(BasePermission):
    """
    Grants access if the requested resource 'belongs' to the same team.
    """

    def has_permission(self, request, view):
        # TODO
        # user_id = request.user.id
        # team_id = request.query_params.get('team_id')
        # coach = Coach.objects.get(user_id=user_id)
        # print(dir(request))
        print(request.args)
        #
        #
        # if coach is not None:
        #     if team_id == coach.team_id:
        #         return True
        # return False
        return True
