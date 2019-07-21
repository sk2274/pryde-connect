import React, { Component } from 'react';
import profilePicture from '../images/profile-picture.png';
import CCEBadge from '../images/cce-badge.svg';
import CornellBadge from '../images/cornell-badge.svg';
import editButton from '../images/edit-button.svg';
import editButtonGreen from '../images/edit-button-green.svg';
import editIcon from '../images/edit-icon.svg';
import editIconGreen from '../images/edit-icon-green.svg';
import CustomDropdown from '../components/CustomDropdown';
import ProfilePictureModal from '../components/ProfilePictureModal';
import { sortOptions, SortableList } from '../components/SortableList';
import styles from '../styles/Profile.module.css';
import api from '../services/api';

class Profile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            user: {
                first_name: "",
                last_name: "",
                role: "",
                displayRole: "",
                locatedAtCornell: false,
                locatedAtCCE: false,
                affiliation: "",
                location: "",
                email: "",
                phone: "",
                website: "",
                researchInterests: [],
                researchDescription: "",
                roles: [],
                ageRanges: [],
                deliveryModes: [],
                researchNeeds: [],
                evaluationNeeds: [],
                projects: []
            },
            statusFilter: "all",
            sortBy: "",
            showModal: false,
            invalidProfile: false
        };
    }

    handleDropdownChange = dropdown => event => {
        this.setState({ [dropdown]: event.target.value });
    }

    showModal = () => {
        this.setState({ showModal: true });
    }

    hideModal = () => {
        this.setState({ showModal: false });
    }

    componentDidMount() {
        const { match } = this.props;

        if (match.url === "/myprofile") {
            api.getLoggedInUser()
                .then(user => this.setState({ user: user }))
                .catch(err => {
                    this.setState({ invalidProfile: true });
                    console.log(err);
                });
        } else {
            const id = match.params.id;
            api.getUserByID(id)
                .then(user => this.setState({ user: user }))
                .catch(err => {
                    this.setState({ invalidProfile: true });
                    console.log(err);
                });
        }
    }

    render() {
        const { user } = this.state;
        const { match } = this.props;
        const statusDropdown = {
            label: "STATUS",
            name: "status",
            options: [
                {
                    value: "all",
                    text: "All"
                },
                {
                    value: "not-started",
                    text: "Not Started"
                },
                {
                    value: "in-progress",
                    text: "In Progress"
                },
                {
                    value: "completed",
                    text: "Completed"
                }
            ],
            handleChange: this.handleDropdownChange("statusFilter")
        };
        const sortDropdown = {
            label: "SORT BY",
            name: "sort",
            options: sortOptions,
            handleChange: this.handleDropdownChange("sortBy")
        };
        let projectsDisplay;
        if (user.projects.length === 0) {
            projectsDisplay = <h2>No projects yet.</h2>
        } else {
            if (this.state.statusFilter === "all") {
                projectsDisplay = <SortableList sortBy={this.state.sortBy} list={user.projects} />
            } else {
                if (user.projects.filter(project=> project.status === this.state.statusFilter).length === 0) {
                    projectsDisplay = <h2>No projects matching filter.</h2>
                } else {
                    projectsDisplay = <SortableList sortBy={this.state.sortBy} list={user.projects.filter(project=> project.status === this.state.statusFilter)} />
                }
            }
        }

        return (
            <div className={styles.container}>
            {
                !this.state.invalidProfile ?
                <>
                <header className={user.role === "Practitioner" ? `${styles.profileHeader} ${styles.practitioner}` : `${styles.profileHeader} ${styles.researcher}`}>
                    <div className={styles.profilePicture}>
                        <img src={profilePicture} alt="Profile pic" />
                        <button className={styles.profilePictureEdit} onClick={this.showModal}>
                            {
                                user.role === "Practitioner" ?
                                    <img src={editIcon} alt="Edit button" />
                                :
                                    <img src={editIconGreen} alt="Edit button" />
                            }
                        </button>
                        <ProfilePictureModal visible={this.state.showModal} handleClose={this.hideModal} />
                    </div>
                    <div className={styles.personalInformation}>
                        <h1>
                            {`${user.first_name} ${user.last_name}`}
                            { user.locatedAtCCE && <img className={styles.CCEBadge} src={CCEBadge} alt="CCE badge" /> }
                            { user.locatedAtCornell && <img className={styles.CornellBadge} src={CornellBadge} alt="Cornell badge" /> }
                        </h1>
                        <h2>{user.displayRole}</h2>
                        <h2>{user.affiliation}</h2>
                        <h2>{user.location}</h2>
                    </div>
                    <div className={styles.contactInformation}>
                        <ul>
                            <li>
                                <a href={`mailto:${user.email}`}>{user.email}</a>
                            </li>
                            {
                                user.phone !== "" &&
                                <li>
                                    <a href={`tel:${user.phone}`}>({user.phone.slice(2, 5)})-{user.phone.slice(5, 8)}-{user.phone.slice(8, 12)}</a>
                                </li>
                            }
                            {
                                user.website !== "" &&
                                <li>
                                    <a href={user.website} target="_blank" rel="noopener noreferrer">{user.website.replace(/(^\w+:|^)\/\//, '')}</a>
                                </li>
                            }
                        </ul>
                    </div>
                    <button id={styles.editProfile}>
                        {
                            user.role === "Practitioner" ?
                                <img src={editButton} alt="Edit button" />
                            :
                                <img src={editButtonGreen} alt="Edit button" />
                        }
                    </button>
                </header>
                <main className={styles.profileContent}>
                    <section className={styles.profileSummary}>
                        <h1>PROFILE</h1>
                        <div>
                            <h2>Research Interests</h2>
                            <ul>
                                {
                                    user.researchInterests.map((interest, idx) => <li key={idx}>{interest}</li>)
                                }
                            </ul>
                            {
                                user.role === "Practitioner" ?
                                    <>
                                        <h2>Roles</h2>
                                        <ul>
                                            {
                                                user.roles.map((role, idx) => <li key={idx}>{role}</li>)
                                            }
                                        </ul>
                                        <h2>Age Range</h2>
                                        <ul>
                                            {
                                                user.ageRanges.map((ageRange, idx) => <li key={idx}>{ageRange}</li>)
                                            }
                                        </ul>
                                        <h2>Delivery Modes</h2>
                                        <ul>
                                            {
                                                user.deliveryModes.map((mode, idx) => <li key={idx}>{mode}</li>)
                                            }
                                        </ul>
                                        <hr />
                                        <h2>Research Needs</h2>
                                        <p>{user.researchNeeds ? user.researchNeeds : "None."}</p>
                                        <h2>Evaluation Needs</h2>
                                        <p>{user.evaluationNeeds ? user.evaluationNeeds : "None."}</p>
                                    </>
                                :
                                    <>
                                        <hr />
                                        <h2>Research Description</h2>
                                        <p>{user.researchDescription}</p>
                                    </>
                            }

                        </div>
                    </section>
                    <section className={styles.projects}>
                        <div className={styles.projectsHeader}>
                            <h1>VIEW PROJECTS</h1>
                            <div>
                                <CustomDropdown {...statusDropdown} />
                                <CustomDropdown {...sortDropdown} />
                            </div>
                        </div>
                        <div>
                            { projectsDisplay }
                        </div>
                    </section>
                </main>
                </>
                :
                <section className={styles.profileNotFound}>
                    <div>
                        <h1>Oops!</h1>
                        {
                            match.url === "/myprofile" ?
                            <p>An error occurred while accessing your profile page. Please log out and log back in again.</p>
                            :
                            <p>We can't seem to find the profile page you're looking for.</p>
                        }
                    </div>
                </section>
            }
            </div>
        );
    }
}

export default Profile;
