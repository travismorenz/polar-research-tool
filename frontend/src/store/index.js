const projectSchema = {
  id: "",
  name: "",
  articleIds: [],
  libraryIds: [],
  isLoading: false,
};

export const initialState = {
  username: "",
  isLoggedIn: false,
  projects: {
    _default: {
      ...projectSchema,
      id: "_default",
      name: "None",
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
      const { projectId, articleIds, libraryIds } = action.payload;
      state.projects[projectId].articleIds = articleIds;
      state.projects[projectId].libraryIds = libraryIds;
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
            ...projectSchema,
            id,
            name,
          };
      });
      break;
    case "logout":
      return { ...initialState };
    default:
      return state;
  }
};
