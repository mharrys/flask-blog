<label for="perPage">Per page</label>
<select id="perPage">
  <option value="1">1</option>
  <option value="5">5</option>
  <option value="10">10</option>
</select>

<label for="orderBy">Order by</label>
<select id="orderBy">
  <% _.each( orderingOptions, function( option ) { %>
    <option value="<%= option.value %>"><%= option.text %></option>
  <% }); %>
</select>

<label for="search">Search</label>
<input id="search" type="text" />
