from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    GET, HEAD, OPTIONS ကဲ့သို့ ဖတ်ရုံသက်သက် Request များကို လူတိုင်းခွင့်ပြုပြီး၊
    ဒေတာပြင်ဆင်မည့် Request များကို Admin သာ ခွင့်ပြုမည့် Custom Permission ခံတံတိုင်း
    """

    def has_permission(self, request, view):
        # 🌟 ၁။ အကယ်၍ ဝင်လာသော HTTP Request သည် SAFE_METHODS (GET, HEAD, OPTIONS) ဖြစ်ပါက True ပေးလိုက်သည်
        # ဆိုလိုသည်မှာ အကောင့်ဝင်ထားစရာပင်မလိုဘဲ Public ပေးကြည့်မည် ဖြစ်သည်။
        if request.method in permissions.SAFE_METHODS:
            return True

        # 🌟 ၂။ အကယ်၍ SAFE_METHODS မဟုတ်ဘဲ POST, PUT, DELETE ဖြစ်လာပါက
        # Request ပို့သူသည် အကောင့်ဝင်ထားသူ ဖြစ်ရမည့်အပြင် Staff/Admin (`is_staff=True`) ဖြစ်မှသာ True ပေးမည်
        return bool(request.user and request.user.is_staff)


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    GET Request ကိုပါ Django ၏ view_model permission ရှိမရှိ တိကျစွာ လိုက်လံစစ်ဆေးပေးမည့် အဆင့်မြင့်တံတိုင်း
    """

    def __init__(self):
        # 🌟 မူလ DjangoModelPermissions ၏ စည်းမျဉ်းမြေပုံ (perms_map) ထဲသို့
        # GET နှင့် HEAD အတွက် 'view_%s' permission လိုက်စစ်ပါဟု ဒိုင်နမစ် သွားရောက်ဖြည့်စွက်လိုက်ခြင်း ဖြစ်သည်။
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['HEAD'] = ['%(app_label)s.view_%(model_name)s']
