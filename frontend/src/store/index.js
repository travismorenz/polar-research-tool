const createProject = ({ name, id }) => ({
  name,
  id,
  pages: [],
  isLoading: false,
});

export const initialState = {
  username: "",
  isLoggedIn: false,
  projects: {
    _default: createProject({ name: "None", id: "_default" }),
  },
  articles: {},
  selectedProjectId: "_default",
};

export const reducer = (state, action) => {
  switch (action.type) {
    case "set_pages_loaded": {
      const { projectId, pages, count } = action.payload;
      state.projects[projectId].count = count;
      state.projects[projectId].pages = pages;
      state.projects[projectId].isLoading = false;
      break;
    }
    case "set_pages_loading":
      state.projects[action.payload].isLoading = true;
      break;
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
      action.payload.projects.forEach((p) => {
        if (!state.projects[p.id])
          state.projects[p.id] = createProject(p, p.id);
      });
      break;
    case "logout":
      return { ...initialState };
    default:
      return state;
  }
};
