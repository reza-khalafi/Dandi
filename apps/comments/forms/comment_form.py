from django import forms
from apps.comments.models.comment import Comment


class CommentForm(forms.ModelForm):
    """
    Form for authenticated users to post comments.
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'دیدگاه یا تجربه ارزشمند خود را در مورد این مقاله بنویسید...',
            'class': 'w-full px-4 py-3 rounded-2xl border border-border-color bg-card-bg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-brand-orange/60 focus:border-brand-orange transition duration-200 resize-none text-sm leading-relaxed'
        }),
        max_length=1500,
        required=True
    )

    class Meta:
        model = Comment
        fields = ['content']
