export const initialState = {
  username: "",
  isLoggedIn: false,
  projects: {
    _default: {
      id: "_default",
      name: "None",
      articleIds: [],
      isLoading: false,
    },
  },
  articles: {},
  selectedProjectId: "_default",
};

export const reducer = (state, action) => {
  switch (action.type) {
    case "add_articles":
      action.payload.forEach((a) => (state.articles[a.id] = { ...a }));
      break;
    case "set_article_ids": {
      const { projectId, ids } = action.payload;
      state.projects[projectId].articleIds = ids;
      break;
    }
    case "set_project_loading": {
      const { projectId, bool } = action.payload;
      state.projects[projectId].isLoading = bool;
      break;
    }
    case "set_count": {
      const { projectId, count } = action.payload;
      state.projects[projectId].count = count;
      break;
    }
    case "select_project":
      state.selectedProjectId = action.payload;
      break;
    case "login":
      state.isLoggedIn = true;
      state.username = action.payload.username;
      // Fill out each pulled in project with needed fields
      action.payload.projects.forEach(({ id, name }) => {
        if (!state.projects[id])
          state.projects[id] = {
            id,
            name,
            articleIds: [],
            isLoading: false,
          };
      });
      break;
    case "logout":
      return { ...initialState };
    default:
      return state;
  }
};
