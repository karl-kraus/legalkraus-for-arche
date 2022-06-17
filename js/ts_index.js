const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
    server: {
      apiKey: "tbuqzVnBrxDVB0WSelohgwffwiQtkukg", // Be sure to use an API key that only allows search operations
      nodes: [
        {
          host: "1ckxuotadbr6fqh3p-1.a1.typesense.net",
          port: "443",
          protocol: "https",
        },
      ],
      cacheSearchResultsForSeconds: 2 * 60, // Cache search results from server. Defaults to 2 minutes. Set to 0 to disable caching.
    },
    // The following parameters are directly passed to Typesense's search API endpoint.
    //  So you can pass any parameters supported by the search endpoint below.
    //  query_by is required.
    additionalSearchParameters: {
      query_by: "full_text"
    },
  });


const searchClient = typesenseInstantsearchAdapter.searchClient;
const search = instantsearch({
    indexName: 'legalkraus',
    searchClient,
});

search.addWidgets([
    instantsearch.widgets.searchBox({
        container: '#searchbox',
    }),

    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            empty: 'No results',
            item: `
                <h4> {{ id }}</h4>
                <h5><a href="{{ id }}.html">{{ title }}</a></h5>
                <p>{{#helpers.snippet}}{ "attribute": "full_text" }{{/helpers.snippet}}</p>
            `
        }
    }),

    instantsearch.widgets.stats({
        container: '#stats-container'
    }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list-persons',
        attribute: 'persons',
        searchable: true,
    }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list-places',
        attribute: 'places',
        searchable: true,
    }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list-orgs',
        attribute: 'orgs',
        searchable: true,
    }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list-works',
        attribute: 'works',
        searchable: true,
    }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list-keywords',
        attribute: 'keywords',
        searchable: true,
    }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list-materials',
        attribute: 'materials',
        searchable: true,
    }),

    instantsearch.widgets.pagination({
        container: '#pagination',
        padding: 2,
    }),
    instantsearch.widgets.clearRefinements({
        container: '#clear-refinements',
    })


]);



search.addWidgets([
    instantsearch.widgets.configure({
        attributesToSnippet: ['full_text'],
    })
]);


search.start();