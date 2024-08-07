from django.shortcuts import render
from django.http import HttpResponse
import os
from .analysis import preprocess_text, analyze_frequency, word_search

def home(request):
    return render(request, '/Users/kasehaas/Desktop/BOM Project/myproject/searchapp/templates/searchapp/home.html')

def results(request):
    search_word = request.GET.get('search_word', '').strip().lower()
    bom_path = os.path.join('/Users/kasehaas/Desktop/BOM Project/book_of_mormon_1830.txt')
    journal1_path = os.path.join('/Users/kasehaas/Desktop/BOM Project/journal_1832_1834.txt')
    journal2_path = os.path.join('/Users/kasehaas/Desktop/BOM Project/journal_1835_1836.txt')

    bom_tokens = preprocess_text(bom_path)
    journal1_tokens = preprocess_text(journal1_path)
    journal2_tokens = preprocess_text(journal2_path)

    bom_frequency, bom_total_words, _ = analyze_frequency(bom_tokens)
    journal1_frequency, journal1_total_words, _ = analyze_frequency(journal1_tokens)
    journal2_frequency, journal2_total_words, _ = analyze_frequency(journal2_tokens)

    if search_word:
        bom_count = word_search(bom_frequency, search_word)
        journal1_count = word_search(journal1_frequency, search_word)
        journal2_count = word_search(journal2_frequency, search_word)
        return render(request, 'results.html', {
            'search_word': search_word,
            'bom_count': bom_count,
            'journal1_count': journal1_count,
            'journal2_count': journal2_count,
            'bom_total_words': bom_total_words,
            'journal1_total_words': journal1_total_words,
            'journal2_total_words': journal2_total_words,
        })
    else:
        return render(request, 'home.html', {'error': 'No word entered.'})

