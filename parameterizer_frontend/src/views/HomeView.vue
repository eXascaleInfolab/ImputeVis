<template xmlns="http://www.w3.org/1999/html">
  <main class="home" style="margin-right: 20px">
    <h3 class="mb-4 text-center" style="margin-top: 50px;">ImputeVIS</h3>
    <p class="text-center">
      ImputeVis is an online tool that allows visualization, parameterization, and optimization of time series
      imputation algorithms.
      <br/>
      This tool was created at the <a href="http://exascale.info/" target="_blank">eXascale Infolab</a>, a research group
      at the <a href="http://www.unifr.ch/" target="_blank">University of Fribourg</a>, Switzerland.
    </p>

    <h4 class="text-center" style="margin-top: 50px;"><strong>Features</strong></h4>
    <br/>

    <div class="row justify-content-center">

      <!-- First Column for Compare -->
      <div class="col-md-2" style="margin-left:170px;">
        <p><b>Datasets</b></p>
        <ul>
          <li>
            <RouterLink to="/display">Display</RouterLink>
          </li>
          <li>
            <RouterLink to="/feature_extraction">Features</RouterLink>
          </li>
        </ul>
      </div>

      <!-- Second Column for Algorithms -->
      <div class="col-md-2">
        <p><b>Data Repair</b></p>
        <ul>
          <li>
            <RouterLink to="/contamination">Contaminate</RouterLink>
          </li>
          <li>
            <RouterLink to="/imputation">Impute</RouterLink>
          </li>
        </ul>
      </div>

       <div class="col-md-2">
        <p><b>Optimization</b></p>
        <ul>
          <li>
            <RouterLink to="/auto_optimizer">Auto-ML Opt.</RouterLink>
          </li>
          <li>
            <RouterLink to="/user_optimizer">User-defined  Opt.</RouterLink>
          </li>
        </ul>
      </div>

      <!-- Third Column for Algorithm Optimization -->
      <div class="col-md-2">
        <p><b>Explanation</b></p>
        <ul>

          <li>
            <RouterLink to="/explainers">Explainer</RouterLink>
          </li>

        </ul>
      </div>




       <div class="row justify-content-center">
        <div  class="col-md-9">
         <hr style="margin: 5%;">

         <h4><strong>Publications</strong></h4>
          <ol>
              <li>Mourad Khayati, Quentin Nater, and Jacques Pasquier. <strong>“ImputeVIS: An Interactive Evaluator to Benchmark Imputation Techniques for Time Series Data.”</strong> In <i>Proceedings of the VLDB Endowment (to Appear)</i>, 2024</li>
              <li>Mourad Khayati, Ines Arous, Zakhar Tymchenko, and Philippe Cudré-Mauroux. <strong>“ORBITS: Online Recovery of Missing Blocks in Multiple Time Series Streams.”</strong> In <i>Proceedings of the VLDB Endowment</i>, Vol. 14, 2021</li>
              <li>Mourad Khayati, Alberto Lerner, Zakhar Tymchenko, and Philippe Cudré-Mauroux. <strong>“Mind the Gap: An Experimental Evaluation of Imputation of Missing Values Techniques in Time Series.”</strong> In <i>Proceedings of the VLDB Endowment</i>, Vol. 13, 2020.</li>
              <li>Ines Arous, Mourad Khayati, Philippe Cudré-Mauroux, Ying Zhang, Martin Kersten, and Svetlin Stalinlov. <strong>“RecovDB: Accurate and Efficient Missing Blocks Recovery for Large Time Series.”</strong> In <i>35th IEEE International Conference on Data Engineering (ICDE 2019)</i>. Macau, China, 2019.</li>
          </ol>
        </div>
       </div>
    </div>


    <!--<p>
      Its primary features empower users to:
      <ul>
        <li>Conduct a comprehensive comparison between CDRec, IIM, M-RNN, and ST-MVL based on imputation metrics such as
          RMSE, MAE, MI, and correlation.<br>
          Within this context, users are endowed with the capability to:
          <ul>
            <li>
              Opt between various configurations:
              those recommended by the thesis author, default parameters delineated in the
              original algorithm papers, or parameters optimized through techniques like Bayesian Optimization, Particle
              Swarm Optimization, or Successive Halving.
            </li>
            <li>
              Obtain metrics including RMSE, MAE, MI, and CORR of the chosen configuration.

            </li>
            <li>
              Visualize the resulting imputations for each algorithm, dependant on the data set.

            </li>
          </ul>

        </li>
        <li>
          Fine-tune individual algorithm parameters for imputation tasks on predefined datasets, during which they can
          access the aforementioned metrics and visualization.
        </li>
        <li>
          Employ distinct optimization strategies, such as Bayesian Optimization, Particle Swarm Optimization, or
          Successive Halving, to pinpoint optimal parameters for a dataset and derive the associated metrics and visual
          insights.
        </li>
        <li>
          Scrutinize the characteristics of individual data sets using the Catch-22 methodology.

        </li>
      </ul>
    </p>-->


  </main>

</template>

<script lang="ts">
import {defineComponent} from "vue";
import {RouterLink} from "vue-router";

export default defineComponent({
  components: {RouterLink}
})
</script>
<style scoped>
.home {
  margin-left: 35px; /* Change this value to increase or decrease the margin */
}
</style>

