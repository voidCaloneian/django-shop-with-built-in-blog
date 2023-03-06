from blogApp.models import Article

def search(search_for):
    "Форма поиска статьи по тегам статьи, названию и описанию"
    return [
        article for article in Article.objects.all() 
        
        if search_for.lower() in article.tags.lower() or 
           search_for.lower() in article.title.lower() or 
           search_for.lower() in article.description.lower()
    ]