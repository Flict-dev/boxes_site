import factory

from reviews.models import Reviews


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reviews

    text = factory.sequence(lambda n: f'Test text - {n}')

    @factory.post_generation
    def author(self, create, extracted):
        if not create:
            return
        if extracted:
            self.author = extracted
