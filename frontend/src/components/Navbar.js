import React from 'react';
import { Link, withRouter } from 'react-router-dom';
import styles from '../styles/Navbar.module.css';
import logo from '../images/pryde-symbol.png';
import api from '../services/api/api';

const Navbar = props => {
    const { loggedIn } = props;

    const handleLogout = () => {
        api.logout();
        props.setLoggedOut();
        props.history.push("/login")
    }

    return (
        <nav className={styles.navbar}>
            <div className={styles.logo}>
                <Link to="/">
                    <img src={logo} alt="PRYDE logo" />
                    <p>
                        <span id={styles.pryde}>PRYDE</span>
                        <br/>
                        <span id={styles.name}>Research Connect</span>
                    </p>
                </Link>
            </div>
            <div className={styles.linksContainer}>
                <Link className={styles.link} to="/browse">
                    BROWSE
                </Link>
                <Link className={styles.link} to="/submit">
                    SUBMIT A PROJECT
                </Link>
                {
                    loggedIn ?
                    <>
                        <Link className={styles.link} to="/myprofile">
                            MY PROFILE
                        </Link>
                        <button className={styles.link} onClick={handleLogout}>
                            LOGOUT
                        </button>
                    </>
                    :
                    <>
                        <Link className={styles.link} to="/login">
                            LOGIN
                        </Link>
                        <Link className={styles.link} to="/signup">
                            SIGNUP
                        </Link>
                    </>
                }
            </div>
        </nav>
    );
}

export default withRouter(Navbar);
