from django import forms
from .models import Profile, User, Question, Tag, Answer
from django.db.models import ObjectDoesNotExist


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login"


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    upload_avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login"

    def clean_repeat_password(self):
        password = self.cleaned_data["password"]
        repeat_password = self.cleaned_data["repeat_password"]
        if password != repeat_password:
            raise forms.ValidationError("Passwords must match")
        return repeat_password

    def save(self):
        self.cleaned_data.pop("repeat_password")
        avatar = self.cleaned_data.pop("upload_avatar")
        user = User.objects.create_user(**self.cleaned_data)
        if avatar is None:
            Profile(user=user).save()
        else:
            Profile(user=user, avatar=avatar).save()


class ProfileEditForm(forms.ModelForm):
    upload_avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, user_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login"
        self.user_id = user_id

    def clean(self):
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = None
        if isinstance(user, User) and user.id != self.user_id:
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def save(self):
        user = User.objects.get(id=self.user_id)
        if user.username != self.cleaned_data["username"] or \
                user.first_name != self.cleaned_data["first_name"] or \
                user.last_name != self.cleaned_data["last_name"] or \
                user.email != self.cleaned_data["email"]:
            user.username = self.cleaned_data["username"]
            user.first_name = self.cleaned_data["first_name"]
            user.last_name = self.cleaned_data["last_name"]
            user.email = self.cleaned_data["email"]
            user.save()
        profile = user.profile
        avatar = self.cleaned_data["upload_avatar"]
        if avatar is not None:
            if not avatar:
                avatar = Profile.avatar.field.default
            profile.avatar = avatar
            profile.save()


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False, max_length=150)

    class Meta:
        model = Question
        fields = ["title", "text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].widget.attrs["placeholder"] = "tag1, tag2, example"

    def clean_tags(self):
        tags_list = self.cleaned_data["tags"].split(",")
        for tag in tags_list:
            if len(tag.strip()) > 20:
                raise forms.ValidationError("Exceeded the maximum tag length (20 characters)")
        return self.cleaned_data["tags"]

    def save(self, user: User) -> int:
        tags_list = self.cleaned_data["tags"].split(",")
        exists_tags = []
        new_tags = []
        for tag in tags_list:
            tag_name = tag.strip()
            try:
                exists_tags.append(Tag.objects.get(name=tag_name))
            except ObjectDoesNotExist:
                new_tags.append(Tag(name=tag_name))
        Tag.objects.bulk_create(new_tags)
        question = Question(title=self.cleaned_data["title"], text=self.cleaned_data["text"], author=user.profile)
        question.save()
        question.tags.set(new_tags + exists_tags)
        return question.id


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].label = "Answer"

    def save(self, user: User, question: Question) -> int:
        answer = Answer(text=self.cleaned_data["text"], question=question, author=user.profile)
        answer.save()
        return answer.id
