# import rules
# from .models import PermissionType


# @rules.predicate
# def is_admin(user):
#     return user.permission_type == PermissionType.ADMIN.value
#     # admin_role = Role.objects.filter(type=RoleType.ADMIN).first()
#     # admin_group = org.rolegroup_set.filter(role=admin_role).first()
#     # if admin_group and admin_group.user.filter(id=user.id).exists():
#     #     return True

# @rules.predicate
# def is_normal(user):
#     return user.permission_type == PermissionType.NORMAL.value
#     # editor_role = Role.objects.filter(type=RoleType.EDITOR).first()
#     # editor_group = org.rolegroup_set.filter(role=editor_role).first()
#     # if editor_group and editor_group.user.filter(id=user.id).exists():
#     #     return True

# # @rules.predicate
# # def is_viewer(user, org):
#     # viewer_role = Role.objects.filter(type=RoleType.VIEWER).first()
#     # viewer_group = org.rolegroup_set.filter(role=viewer_role).first()
#     # if viewer_group and viewer_group.user.filter(id=user.id).exists():
#     #     return True

# # rules.add_perm('accounts.view_org', is_admin | is_editor)
# # rules.add_perm('apps.view_org', is_admin | is_editor)
# rules.add_perm('accounts.admin', is_admin)
# rules.add_perm('accounts.normal', is_admin | is_normal)