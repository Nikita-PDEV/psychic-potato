from flask_login import current_user  
from flask import abort  

class AuthorRequiredMixin:  
    @classmethod  
    def is_author(cls, group_name='authors'):  
        # Проверка, принадлежит ли пользователь к указанной группе  
        if current_user.groups is None or group_name not in [group.name for group in current_user.groups]:  
            abort(403, description=f"У вас нет прав доступа к этой функции. Необходима группа: '{group_name}'")  # Запрет доступа