from haystack.forms import FacetedSearchForm

class RoomSearchForm(FacetedSearchForm):
    def search(self):
        if hasattr(self, 'cleaned_data'):
            query = self.cleaned_data.get('q')
        else:
            query = '*'
        sqs = self.searchqueryset.raw_search(query)

        if self.load_all:
            sqs = sqs.load_all()

        for facet in self.selected_facets:
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))
        return sqs
    