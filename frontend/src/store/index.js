export const initialState = {
  username: "",
  isLoggedIn: false,
  isAdmin: false,
  projects: {
    _default: {
      id: "_default",
      name: "None",
    },
  },
  selectedProjectId: "_default",
};

export const reducer = (state, action) => {
  switch (action.type) {
    case "remove_project":
      delete state.projects[action.payload];
      break;
    case "add_project":
      state.projects[action.payload.id] = {
        ...action.payload,
      };
      break;
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
