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
