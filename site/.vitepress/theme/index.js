import DefaultTheme from 'vitepress/theme'
import HomeQuote from './HomeQuote.vue'
import QuoteList from './QuoteList.vue'
import TermList from './TermList.vue'
import BookList from './BookList.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('HomeQuote', HomeQuote)
    app.component('QuoteList', QuoteList)
    app.component('TermList', TermList)
    app.component('BookList', BookList)
  }
}
