import React, { useContext } from "react";
import { Link } from "react-router-dom";

import { AppContext } from "./App";
import { logout } from "../services/auth";

const Navbar = () => {
  const {
    state: { isLoggedIn, username, projects, selectedProjectId },
    action,
  } = useContext(AppContext);

  const handleLogout = async () => {
    await logout();
    action("logout");
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
                    value={selectedProjectId}
                    onChange={(e) => action("select_project", e.target.value)}
                  >
                    {Object.values(projects).map((p) => (
                      <option value={p.id} key={p.id}>
                        {p.name}
                      </option>
                    ))}
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
                    <button className="logout-btn" onClick={handleLogout}>
                      Logout
                    </button>
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
