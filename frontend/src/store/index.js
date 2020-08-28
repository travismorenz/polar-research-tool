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
  isAdmin: false,
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
    case "set_keyphrases": {
      const { projectId, keyphrases } = action.payload;
      state.projects[projectId].keyphrases = keyphrases;
      break;
    }
    case "set_categories": {
      const { projectId, categories } = action.payload;
      state.projects[projectId].categories = categories;
      break;
    }
    case "add_articles":
      action.payload.forEach((a) => (state.articles[a.id] = { ...a }));
      break;
    case "set_article_ids": {
      const { projectId, articleIds } = action.payload;
      state.projects[projectId].articleIds = articleIds;
      break;
    }
    case "set_library_ids": {
      const { projectId, libraryIds } = action.payload;
      state.projects[projectId].libraryIds = libraryIds;
      break;
    }
    case "toggle_in_library": {
      const { projectId, articleId } = action.payload;
      const library = state.projects[projectId].libraryIds;
      if (library.includes(articleId)) {
        state.projects[projectId].libraryIds = state.projects[
          projectId
        ].libraryIds.filter((id) => id !== articleId);
      } else {
        state.projects[projectId].libraryIds.push(articleId);
      }
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
    case "login": {
      const { username, projects, isAdmin } = action.payload;
      state.isLoggedIn = true;
      state.username = username;
      state.isAdmin = !!isAdmin;
      // Fill out each pulled in project with needed attributes
      projects.forEach((project) => {
        if (!state.projects[project.id])
          state.projects[project.id] = {
            ...projectSchema,
            ...project,
          };
      });
      break;
    }
    case "logout":
      return { ...initialState };
    default:
      return state;
  }
};
