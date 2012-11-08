% if detail == 'list':
  % if strategy:
    <a class="strategy" href="/{{strategy.repository.state.identifier}}/integration-strategies#{{path}}">
      {{!'<span class="error">☐</span>' if not strategy.tests else '☑'}} {{strategy.title}} <span>{{path}}</span>
    </a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if strategy:
    <dt><h2 id="{{path}}">{{!'<span class="error">☐</span>' if not strategy.tests else '☑'}} {{strategy.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td>{{!strategy.description}}</td>
        </tr>
        % if strategy.tags:
          <tr>
            <th>Tags</th>
            <td>
              <ul>
                % for path, tag in strategy.tags.iteritems():
                  <li>
                    % include tag path=path, tag=tag, detail='list'
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
        <tr> 
          <th>Parent</th>
          <td>
            <p>
              % path, architecture = strategy.parent
              % if path:
                % include architecture path=path, architecture=architecture, detail='list'
              % else:
                <span class="error">No parent specified</span>
              % end
            </p>
          </td>
        </tr>
        % if strategy.mapped_here:
          <tr>
            <th>Requirements</th>
            <td>
              <ul>
                % for path, requirement in strategy.mapped_here.iteritems():
                  <li>
                    % include requirement path=path, requirement=requirement, detail='list'
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
        <tr>
          <th>Tests</th>
          <td>
            % if strategy.tests:
              <ul>
                % for path, test in strategy.tests.iteritems():
                  <li>
                    % include test path=path, test=test, detail='list'
                  </li>
                % end
              </ul>
            % else:
              <p class="error">No tests specified.</p>
            % end
          </td>
        </tr>
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
