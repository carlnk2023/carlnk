from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def profile_complete_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.profile_complete:
            return redirect('setup_account')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
