import React, { useContext } from "react";
import { Link } from "react-router-dom";

import { AppContext, initialState } from "./App";
import logout from "../services/logout";

const Navbar = () => {
  const {
    state: { isLoggedIn, username, projects, selectedProject },
    setState,
  } = useContext(AppContext);

  const handleLogout = async () => {
    await logout();
    setState(initialState);
  };

  return (
    <header>
      <div className="navbar container grid-xl">
        <div className="navbar-section">
          <Link to="/" className="navbar-brand mr-10">
            POLAR <span>Research Tool</span>
          </Link>
        </div>
        <div className="navbar-section">
          {isLoggedIn ? (
            <>
              <div className="form-group">
                Selected Project:
                <label className="form-inline">
                  <select
                    className="form-select"
                    id="project-select"
                    value={selectedProject}
                    onChange={(e) => {
                      e.persist();
                      setState((s) => ({
                        ...s,
                        selectedProject: e.target.value,
                      }));
                    }}
                  >
                    {projects.map((p) => (
                      <option value={p.name} key={p.id}>
                        {p.name.charAt(0) + p.name.slice(1)}
                      </option>
                    ))}
                    <option value="">None</option>
                  </select>
                </label>
              </div>
              <div className="dropdown">
                <button className="btn dropdown-toggle">{username} ▼</button>
                <ul className="menu">
                  <li className="menu-item">
                    <Link to="/account">My Account</Link>
                  </li>
                  <li className="menu-item">
                    <a href="#" onClick={handleLogout}>
                      Logout
                    </a>
                  </li>
                </ul>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="btn text-large nav-btn">
                Login
              </Link>
              <Link to="/register" className="btn text-large">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
