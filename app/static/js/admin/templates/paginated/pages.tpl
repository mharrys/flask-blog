<% if ( lastPage > firstPage ) { %>
  <div class="pagination">
    <ul>
      <li <% if ( !prevPage ) { %>class="disabled"<% } %>><a href="#posts" class="prev">&laquo;</a></li>
      <% for ( page = firstPage; page <= lastPage; page++ ) { %>
        <li <% if ( currentPage == page ) { %>class="active"<% } %>><a href="#posts" class="page"><%= page %></a></li>
      <% } %>
      <li <% if ( !nextPage ) { %>class="disabled"<% } %>><a href="#posts" class="next">&raquo;</a></li>
    </ul>
  </div>
<% } %>
