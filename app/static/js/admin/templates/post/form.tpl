<form>
  <p class="text-success"></p>
  <p class="text-error"></p>
  <label for="title">Title</label>
  <input id="title" type="text" class="input-xxlarge" value="<%= title %>"/>
  <label for="markup">Markup</label>
  <textarea id="markup" rows="15" class="input-block-level"><%= markup %></textarea>
  <label class="checkbox">
    <input id="visible" type="checkbox"<% if ( visible ) { %> checked <% } %>> Visible
  </label>
  <p><button class="btn btn-primary">Submit</button></p>
</form>
