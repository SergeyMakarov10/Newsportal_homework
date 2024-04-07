from news.models import *
from django.db.models import F

# 1. Создать двух пользователей (с помощью метода User.objects.create_user).
user1 = User.objects.create_user(username='username1', first_name='FirstName1')
user2 = User.objects.create_user(username='username2', first_name='FirstName2')

# 2. Создать два объекта модели Author, связанные с пользователями.
author1 = Author.objects.create(author_user=user1)
author2 = Author.objects.create(author_user=user2)

# 3. Добавить 4 категории в модель Category.
category1 = Category.objects.create(category_name='Спорт')
category2 = Category.objects.create(category_name='Политика')
category3 = Category.objects.create(category_name='Музыка')
category4 = Category.objects.create(category_name='Наука')

# 4. Добавить 2 статьи и 1 новость.
article1 = Post.objects.create(author=author1, category_type='AR', title='Статья 1', text='Текст 1')
article2 = Post.objects.create(author=author2, category_type='AR', title='Статья 2', text='Текст 2')
news1 = Post.objects.create(author=author2, category_type='NW', title='Новость 1', text='Текст Новости 1')
news2 = Post.objects.create(author=Author.objects.get(id=2), category_type='NW', title='Новость 2', text='Оппозиция заявила о митинге')
Post.objects.filter(id=4).update(text='Оппозиция заявила о митинге')


# 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
PostCategory.objects.create(post=article1, category=category1)
PostCategory.objects.create(post=article1, category=category3)
PostCategory.objects.create(post=article2, category=category2)
PostCategory.objects.create(post=article2, category=category4)
PostCategory.objects.create(post=news1, category=category2)
PostCategory.objects.create(post=news1, category=category3)

# 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
comment1 = Comment.objects.create(comment_post=article1, comment_user=user2, text='Текст комментария 1')
comment2 = Comment.objects.create(comment_post=article1, comment_user=user1, text='Текст комментария 2')
comment3 = Comment.objects.create(comment_post=article2, comment_user=user1, text='Текст комментария 3')
comment4 = Comment.objects.create(comment_post=news1, comment_user=user2, text='Текст комментария 4')
Comment.objects.create(comment_post=Post.objects.get(id=2), comment_user=User.objects.get(id=1), text='Текст комментария 5')

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
# к статьям/новостям
article1.like()
article1.like()
article1.dislike()
article2.like()
article2.like()
article2.like()
news1.like()
news1.like()
news1.dislike()

# к комментариям
comment1.like()
comment1.like()
comment1.dislike()
comment2.like()
comment3.like()
comment3.like()
comment4.dislike()

# 8. Обновить рейтинги пользователей.
Author.objects.get(id=1).update_rating()
Author.objects.get(id=2).update_rating()

# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
Author.objects.order_by('-author_rating').values('author_user__username', 'author_rating').first()

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/
# дислайках к этой статье.
best_article = Post.objects.filter(category_type='AR').order_by('-rating').first()
print('Лучшая статья: ', best_article.creation_date, best_article.author.author_user.username, best_article.rating,
      best_article.title, best_article.preview(), sep='\n')

# Post.objects.filter(category_type='AR').order_by('-rating').values('creation_date', 'author', 'title', 'text').first()

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
comments = Comment.objects.filter(comment_post=best_article)

for c in comments:
    print((f"дата: {c.creation_date}, пользователь: {c.comment_user.username}, "
           f"рейтинг {c.rating}, текст комментария: {c.text}"))

# Или этот вариант для Django shell
for c in Comment.objects.filter(comment_post=Post.objects.filter(category_type='AR').order_by('-rating').first()): print((f"дата: {c.creation_date}, пользователь: {c.comment_user.username}, рейтинг {c.rating}, текст комментария: {c.text}"))