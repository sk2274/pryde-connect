import React from 'react';
import styles from '../../../styles/Map.module.css';

export default class Oswego extends React.Component {
    render() {
        return (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 166 130">
                <title>Oswego</title>
                <g id="Layer_2" data-name="Layer 2">
                    <g id="Layer_2-2" data-name="Layer 2">
                        <path d="M1,68l14-8,7-2S34,45,35,45s15-1,15-1l3,1,15-1,7-2,4-8,5-1-5-4L81,8l34,2-1-9,48,4,3,50-9-3L140,87l6,6-4,36-19-6L85,107l-5-5,1,13-6,1-8-7-1,10-6-8H27v-6H2Z" style={{ fill: `${this.props.color}` }} className={styles.county} onClick={this.props.onClick} />
                    </g>
                </g>
            </svg >
        )
    }
}
