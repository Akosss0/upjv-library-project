import "./LoginForm.css";
import backgroundImage from "../../assets/librairy.png";
import { Link } from "react-router-dom";

export function LoginForm() {
    return (
        <>
            <section className="Form">
                <h1>Se connecter</h1>
                <form action="POST">
                    <div className="formField">
                        <label htmlFor="username">Identifiant</label>
                        <input id="username" type="text" placeholder="c22202083" />
                    </div>
                    <div className="formField">
                        <label htmlFor="password">Mot de passe</label>
                        <input id="password" type="password" placeholder="●●●●●●●●" />
                    </div>
                    <Link className="forgottenPassword" to="">Mot de passe oublié ?</Link>
                    <button type="submit">Se connecter</button>
                    <Link className="button" to="">S'inscrire</Link>
                </form>
                <svg className="backgroundBook" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
                    xmlnsXlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 512 512" xmlSpace="preserve">
                    <path d="M256,74.17c-31.52-27.1-77.22-31.14-118.82-26.98C88.74,52.09,39.84,68.7,9.38,82.55C3.67,85.15,0,90.84,0,97.11v352
    	c0,8.84,7.17,16,16,16c2.28,0,4.54-0.49,6.62-1.44c28.22-12.8,73.7-28.19,117.76-32.64c45.09-4.54,82.88,2.78,103.14,28.06
    	c5.53,6.89,15.6,8,22.49,2.47c0.91-0.73,1.74-1.56,2.47-2.47c20.26-25.28,58.05-32.61,103.1-28.06
    	c44.1,4.45,89.6,19.84,117.79,32.64c8.04,3.66,17.53,0.1,21.19-7.94c0.95-2.08,1.43-4.34,1.44-6.62v-352
    	c0-6.27-3.67-11.96-9.38-14.56c-30.46-13.86-79.36-30.46-127.81-35.36C333.22,43,287.52,47.07,256,74.17z" />
                </svg>
            </section>
            <div className="hero-background">
                <img className="backgroundImage" src={backgroundImage} alt="" />
            </div>
        </>)
}
