route_prefix = '/api/v1/'

# user endpoints
user_endpoint_prefix = f'{route_prefix}account/'

account_register = f'{user_endpoint_prefix}register'
account_detail = f'{user_endpoint_prefix}user'
account_login = f'{user_endpoint_prefix}login'
account_logout = f'{user_endpoint_prefix}logout'
account_delete = f'{user_endpoint_prefix}deactivate'
account_update = f'{user_endpoint_prefix}update'


# post endpoints
post_endpoints_prefix = f'{route_prefix}post/'

post_all = f'{post_endpoints_prefix}all/<page_number>'
post_category = f'{post_endpoints_prefix}<category>/<page_number>'
post_detial = f'{post_endpoints_prefix}detial/<post_id>'
post_image = f'{post_endpoints_prefix}media/<image>'
post_comment = f'{post_endpoints_prefix}comment/add'

# admin endpoints
admin_endpoints_prefix = f'{route_prefix}admin/'

admin_acc_register = f'{admin_endpoints_prefix}register'
admin_post_add = f'{admin_endpoints_prefix}post/new'
admin_post_delete = f'{admin_endpoints_prefix}post/delete'