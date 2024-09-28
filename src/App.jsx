import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './index.css';

function App() {
  const [isBlinking, setIsBlinking] = useState(false);

  const handleButtonClick = () => {
    setIsBlinking(!isBlinking);
  };

  return (
    <>
      <button
        className={isBlinking ? 'blinking' : ''}
        onClick={handleButtonClick}
      >
        {isBlinking ? 'Stop Recording' : 'Start Recording'}
      </button>
    </>
  );
}

export default App;
