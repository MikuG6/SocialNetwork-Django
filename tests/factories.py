# import factory
#
# from factory.django import DjangoModelFactory
#
# from service.models import User, Album
#
#
# class UserFactory(DjangoModelFactory):
#     class Meta:
#         model = User
#
#     username = factory.Sequence(lambda n: f'test{n}')
#     email = factory.Sequence(lambda n: f'test{n}@mail.com')
#     password = factory.PostGenerationMethodCall(
#         'set_password', 'test'
#     )
#
#     @factory.post_generation
#     def has_album(self, create, extracted, **kwargs):
#         if not create:
#             return
#         if extracted:
#             default_album, _ = Album.objects.get_or_create(
#                 name='album',
#                 user=1
#             )
#             Album.objects.get_or_create(default_album)
