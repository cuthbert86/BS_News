import string, random
from django.db.models.signals import pre_save, post_save, pre_delete, post_migrate
from django.dispatch import receiver
from django.utils.text import slugify


def random_string_generator(size=10,
                            chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(getattr(instance, 'headline', '') or random_string_generator(size=6))
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        # Ensure minimum base length for slug before appending '-xxxx'
        base_slug = slug[:max_length-5] if max_length > 5 else ''
        new_slug = f"{base_slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_slug_generator1(instance, new_slug=None):
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(getattr(instance, 'headline', '') or random_string_generator(size=6))
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        # Ensure minimum base length for slug before appending '-xxxx'
        base_slug = slug[:max_length-5] if max_length > 5 else ''
        new_slug = f"{base_slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
