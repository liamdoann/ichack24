// import React, { useEffect, useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import '../App.css';
// import { LineChart } from '@mui/x-charts';

// function PerformanceGraph() {
//   const navigate = useNavigate();
//   const [data, setData] = useState([]);

//   // useEffect(() => {
//   //   const fetchData = async () => {
//   //     try {
//   //       const response = await fetch('http://localhost:5000/performance');
//   //       const data = await response.json();
//   //       setData(data);
//   //     } catch (error) {
//   //       console.error(error);
//   //     }
//   //   };

//   //   fetchData();
//   // }, []);

//   const xData = [1,2,3,4,5,6,7];
//   const seriesData = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0];
//   return (
//     <div className="App">
//       <header className="App-header">
//         <h1>Performance Graph</h1>
        
//         <LineChart
//         xAxis = {[{data: xData}]}
//         series = {[{data: seriesData}]}
//         // width={500}
//         // height={300}
//           // xAxis = {[{data: data.map((d) => d.date)}]}
//           // series = {[data.map((d) => d.percentage)]}
//         />
//         <button onClick={() => navigate('/')} className="button">Back</button>
//       </header>
//     </div>
//   );
// }

// export default PerformanceGraph;