<template>
  <main>
    <div v-if="loadingResults" class="d-flex justify-content-center mt-3">
      <div class="alert alert-info d-flex align-items-center">
        <div class="spinner-border text-primary me-3" role="status"></div>
        Loading...
      </div>
    </div>

    <form ref="ref_reload" @submit.prevent="submitForm">
      <div class="justify-content-right" style="padding: 10px; position: absolute; z-index: 100; right: 0;">
        <normalization-toggle v-model="normalizationMode"></normalization-toggle>
      </div>
    </form>

    <div class="mb-auto">
      <div class="col-lg-12">
        <div class="row me-1">
          <div class="col-lg-10">

            <h3 v-if="naterq_error" style="color : red; margin-left : 20%" >Imputation not found with this pattern and this contamination...</h3>

            <highcharts v-if="imputedData" class="mb-3 pb-3" :options="chartOptionsImputed"></highcharts>
            <highcharts v-if="!imputedData" class="mb-3 pb-3" :options="chartOptionsOriginal"></highcharts>



            <div v-if="metricsCDRec || metricsIIM || metricsMRNN || metricsSTMVL" style="margin-left: 20%; margin-right: 20%; margin-top: 5%; width:60%; text-align:center;">
              <!--<kiviat-display v-if="imputedData" :metrics="{
                CDRec :{rmse_1: rmseCDRec, mae_1: maeCDRec, mi_1: miCDRec, corr_1: corrCDRec },
                IIM :{ rmse_2: rmseIIM, mae_2: maeIIM, mi_2: miIIM, corr_2: corrIIM },
                MRNN :{ rmse_3: rmseMRNN, mae_3: maeMRNN, mi_3: miMRNN, corr_3: corrMRNN },
                STMVL :{ rmse_4: rmseSTMVL, mae_4: maeSTMVL, mi_4: miSTMVL, corr_4: corrSTMVL }
                }" /> -->


              <div v-if="metricsCDRec || metricsIIM || metricsMRNN || metricsSTMVL || imputedData" class="mt-4" style="margin: 3%;">
                <div class="row">
                  <table class="table">
                    <thead>
                    <tr>
                      <th scope="col"></th>
                      <th scope="col" v-if="metricsCDRec">CDRec</th>
                      <th scope="col" v-if="metricsIIM">IIM</th>
                      <th scope="col" v-if="metricsMRNN">M-RNN</th>
                      <th scope="col" v-if="metricsSTMVL">ST-MVL</th>
                    </tr>
                    </thead>
                    <tbody>
                    <!-- Metrics Rows -->
                    <tr>
                      <th scope="row" v-if="rmseCDRec !== null && rmseCDRec !== ''">RMSE</th>
                      <td v-if="metricsCDRec">{{ rmseCDRec }}</td>
                      <td v-if="metricsIIM">{{ rmseIIM }}</td>
                      <td v-if="metricsMRNN">{{ rmseMRNN }}</td>
                      <td v-if="metricsSTMVL">{{ rmseSTMVL }}</td>
                    </tr>
                    <tr>
                      <th scope="row" v-if="maeCDRec !== null && maeCDRec !== ''">MAE</th>
                      <td v-if="metricsCDRec">{{ maeCDRec }}</td>
                      <td v-if="metricsIIM">{{ maeIIM }}</td>
                      <td v-if="metricsMRNN">{{ maeMRNN }}</td>
                      <td v-if="metricsSTMVL">{{ maeSTMVL }}</td>
                    </tr>
                    <tr>
                      <th scope="row" v-if="miCDRec !== null && miCDRec !== ''">MI</th>
                      <td v-if="metricsCDRec">{{ miCDRec }}</td>
                      <td v-if="metricsIIM">{{ miIIM }}</td>
                      <td v-if="metricsMRNN">{{ miMRNN }}</td>
                      <td v-if="metricsSTMVL">{{ miSTMVL }}</td>
                    </tr>
                    <tr>
                      <th scope="row" v-if="corrCDRec !== null && corrCDRec !== ''">CORR</th>
                      <td v-if="metricsCDRec">{{ corrCDRec }}</td>
                      <td v-if="metricsIIM">{{ corrIIM }}</td>
                      <td v-if="metricsMRNN">{{ corrMRNN }}</td>
                      <td v-if="metricsSTMVL">{{ corrSTMVL }}</td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>


          </div>
          <div class="col-lg-2" style="margin-top: 50px;">
            <div class="row me-5">
              <div class="">
                <form ref="ref_missingvalues" @submit.prevent="submitForm">
                  <data-select v-model="dataSelect" @update:seriesNames="updateSeriesNames"/>
                  <scenario-missing-values v-model="scenarioMissingValues" />
                  <div v-if="scenarioMissingValues !== 'blackout'">
                    <div class="checkbox-slider">
                      <div v-for="series in mySeries" :key="series" class="form-check">
                        <input class="form-check-input" type="checkbox" :id="`checkbox-${series}`" :value="series" v-model="selectedSeries"/>
                        <label class="form-check-label" :for="`checkbox-${series}`">{{ series.substring(3) }}</label>
                      </div>
                    </div>
                  </div>

                  <missing-rate v-model="missingRate"/>
                </form>
              </div>
            </div>



            <form ref="ref_algos" @submit.prevent="submitForm">
              <div class="mt-4 me-6">
                <label for="ref_algos" class="form-label" style="font-weight: bold;">Imputation Technique</label>
              <div class="row ms-1">
                <div class="col form-check ">
                  <input class="form-check-input" type="checkbox" value="CDRec" id="CDRec" v-model="checkedNames" checked >
                  <label class="form-check-label" for="CDRec">Matrix-based</label>
                </div>
                <div class="col form-check ">
                  <input class="form-check-input" type="checkbox" value="ST-MVL" id="ST-MVL" v-model="checkedNames">
                  <label class="form-check-label" for="ST-MVL">Pattern-based</label>
                </div>
              </div>
              <div>
                <div class="row ms-1">
                  <div class="col form-check " v-if="nns_checked == true" >
                    <input class="form-check-input" type="checkbox" value="M-RNN" id="MRNN" v-model="checkedNames">
                    <label class="form-check-label" for="MRNN">NNs-based</label>
                  </div>
                  <div class="col form-check " v-if="reg_checked == true">
                    <input class="form-check-input" type="checkbox" value="IIM" id="IIM" v-model="checkedNames">
                    <label class="form-check-label" for="IIM">Regression-based</label>
                  </div>
                </div>
              </div>
                <button type="submit" id="upload_algo" class="btn btn-success" style="margin-top:6px; width:100px; ">Upload</button>
              </div>


              <!-- Parameter Options -->
              <div class="mb-3"  data-toggle="tooltip" data-placement="top" style="margin-top:36px;"
                   title="Also impacts run-time, amount depends on algorithm.">
                <label for="parametrization" class="form-label" style="font-weight: bold;" >Parametrization</label>
                <div class="custom-select">
                  <select class="form-control" name="paramOption" v-model="selectedParamOption">
                    <option value="recommended">Optimal (recommended)</option>
                    <option value="default">Default Params</option>
                    <option value="bayesian_optimization">Bayesian Optimization</option>
                    <option value="pso_optimization">Particle Swarm Optimization</option>
                    <option value="succesive_halving">Successive Halving</option>
                  </select>
                </div>
              </div>

              <div class="d-flexs mt-4 me-10" >
                <button type="submit" id="alpha_run" class="btn btn-primary" style="margin-top:10px;  width:100px; ">Impute</button>
                <button type="submit" id="delta_reset" class="btn btn-danger" style="margin-top:10px; margin-left : 10%; width:100px; ">Reset</button>
              </div>

              <div class="popup" id="popup">
                <label><input type="checkbox" id="nns_based" checked>NNs-based</label><br>
                <label><input type="checkbox" id="reg_based" checked>Regression-based</label><br>

                <input type="file" ref="fileInput" @change="uploadFile" style="margin-top:30px; margin-bottom:20px; width:145px;  "><br />

                <button type="submit" id="validate" className="btn btn-success" style="margin-top:25px; width:100px; ">Validate</button>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style>
  .popup {
    display: none;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    padding: 40px; /* Increase padding for larger popup */
    border: 2px solid #ccc; /* Increase border size for larger popup */
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.4); /* Increase shadow for larger popup */
    z-index: 9999;
    font-size: 25px; /* Increase font size */
  }
  .checkbox-slider {
  height: 65px; /* Set the desired height */
  overflow-y: scroll; /* Enable vertical scrolling */
  border: 1px solid #ccc; /* Optional: Add a border */
  padding: 10px; /* Optional: Add padding */
}

  /* Style for checkboxes */
  .popup input[type="checkbox"] {
    transform: scale(2); /* Increase size of checkboxes */
    margin: 30px; /* Increase margin between checkbox and label */
  }
</style>

<script lang="ts">
import {ref, watch, reactive, shallowReactive} from 'vue';
import { useRoute } from 'vue-router'
import DataSelect from './components/DataSelect.vue';
import MissingRate from './components/MissingRate.vue';
import NormalizationToggle from './components/NormalizationToggle.vue'
import axios from 'axios';
import {Chart} from 'highcharts-vue'
import ScenarioMissingValues from './components/ScenarioMissingValues.vue';

import {IIM_DEFAULTS, CDREC_DEFAULTS, MRNN_DEFAULTS, STMVL_DEFAULTS} from './thesisUtils/defaultParameters';
import {
  createSegmentedSeries,
  createSeries,
  generateChartOptions
} from "@/views/thesisUtils/utils";
import Metrics2Display from "@/views/components/Metrics2Display.vue";
import KiviatDisplay from './components/KiviatDisplay.vue';
import defaultConfig from'./../assets_naterq/default_values.json';


export default {
  components: {
    Metrics2Display,
    KiviatDisplay,
    NormalizationToggle,
    highcharts: Chart,
    DataSelect,
    MissingRate,
    ScenarioMissingValues
  }, setup() {
    const route = useRoute()
    const dataSelect = ref(route.params.datasetName || defaultConfig.loading.load_dataset)
    const normalizationMode = ref(defaultConfig.loading.load_normalization);
    const scenarioMissingValues = ref(defaultConfig.loading.load_scenario);
    const missingRate = ref(defaultConfig.loading.load_missing_rate_contamination); // Default missing rate
    const naterq_error = ref(false); // Whether imputation has been carried out


    let truncationRank = defaultConfig.cdrec.default_reduction_rank;
    let epsilon = defaultConfig.cdrec.default_epsilon_str;
    let iterations = defaultConfig.cdrec.default_iteration;

    let numberSelect = defaultConfig.iim.default_neighbor;
    let typeSelect = ''; // Default selected type is "Normal", denoted by an empty string

    let learningRate = defaultConfig.mrnn.default_learning_rate;
    let hiddenDim = defaultConfig.mrnn.default_hidden_dim;
    let iterationsMRNN = defaultConfig.mrnn.default_iterations;
    let keepProb = defaultConfig.mrnn.default_keep_prob;
    let seqLen = defaultConfig.mrnn.default_sequence_length;

    let windowSize = defaultConfig.stmvl.default_window_size;
    let gamma = defaultConfig.stmvl.default_gamma;
    let alpha = defaultConfig.stmvl.default_alpha;

    let currentSeriesNames = [];
    const mySeries = ref([]);
    const selectedSeries = ref([]);

    const fetchedData = reactive({});
    let loadingResults = ref(false);
    const selectedParamOption = ref('recommended'); // Default option

    //CDRec Parameters
    const rmseCDRec = ref(null);
    const maeCDRec = ref(null);
    const miCDRec = ref(null);
    const corrCDRec = ref(null);
    const metricsCDRec = ref(false);

    //IIM Parameters
    const rmseIIM = ref(null);
    const maeIIM = ref(null);
    const miIIM = ref(null);
    const corrIIM = ref(null);
    const metricsIIM = ref(false);

    // M-RNN Parameters
    const rmseMRNN = ref(null);
    const maeMRNN = ref(null);
    const miMRNN = ref(null);
    const corrMRNN = ref(null);
    const metricsMRNN = ref(false);

    // ST-MVL Parameters
    const rmseSTMVL = ref(null);
    const maeSTMVL = ref(null);
    const miSTMVL = ref(null);
    const corrSTMVL = ref(null);
    const metricsSTMVL = ref(false);

    let obfuscatedMatrix = [];
    let groundtruthMatrix = [];
    const checkedNames = ref([]);
    const imputedData = ref(false); // Whether imputation has been carried out
    const nns_checked = ref(true);
    const reg_checked = ref(true);

    const obfuscatedColors = defaultConfig.colors.chart;

    const fetchData = async () => {

      if (dataSelect.value !== "upload")
      {
        try
        {
          loadingResults.value = true;

          let selection_series = ["-1:test"];
          if (selectedSeries.value.length > 0)
          {
               selection_series = selectedSeries.value;
          }
          if (scenarioMissingValues.value == "blackout")
          {
               selectedSeries.value = mySeries.value;
          }

          const response = await axios.post('http://localhost:8000/api/fetchData/',
              {
                dataset: dataSelect.value,
                normalization : normalizationMode.value,
                scenario : scenarioMissingValues.value,
                missing_rate: missingRate.value,
                selected_series: selection_series
              },
              {
                headers:
                {
                  'Content-Type': 'application/text',
                }
              }
          );

          chartOptionsOriginal.value.series.splice(0, chartOptionsOriginal.value.series.length);
          clearErrorMetrics();

          obfuscatedMatrix = response.data.matrix;
          groundtruthMatrix = response.data.groundtruth;
          obfuscatedMatrix.forEach((data: number[], index: number) => {
              chartOptionsOriginal.value.series[index] = createSeries(index, data, dataSelect.value, currentSeriesNames[index], 'line', 2, obfuscatedColors[index])
          });
          if (missingRate.value != "0")
          {
            groundtruthMatrix.forEach((data: number[], index: number) => {
              if (selection_series.some(sel => sel.includes(currentSeriesNames[index].toString())))
              {
                  chartOptionsOriginal.value.series.push(createSeries(index, data, dataSelect.value, currentSeriesNames[index] + "_MV", 'dash', 2, obfuscatedColors[index], false));
              }
            });
          }

          mySeries.value = []
          for (let i = -1; i < currentSeriesNames.length && i < 4; i++)
          {
            mySeries.value.push(`${i + 1}: ${currentSeriesNames[i+1]}`);
          }

        } catch (error)
        {
          console.error(error);
          naterq_error.value = true;

        } finally {
          naterq_error.value = false;
          loadingResults.value = false;
        }
      }
    }

    const fetchParameters = async () => {
      if (dataSelect.value !== "upload")
      {
        if (selectedParamOption.value !== 'default')
        {
          try {
            const dataAbbreviation = getCategory(dataSelect.value);

            const response = await axios.post('http://localhost:8000/api/fetchParameters/',
                {
                  data_set: dataAbbreviation,
                  normalization: normalizationMode.value,
                  param_options: selectedParamOption.value
                },
                {
                  headers: {
                    'Content-Type': 'application/text',
                  }
                }
            );
            const parameters = response.data.params;

            // CDRec Parameters
            truncationRank = parameters['cdrec'][dataAbbreviation].best_params.rank || truncationRank;
            epsilon = parameters['cdrec'][dataAbbreviation].best_params.eps || epsilon;
            iterations = parameters['cdrec'][dataAbbreviation].best_params.iters || iterations;

            // IIM Parameters
            numberSelect = parameters['iim'][dataAbbreviation].best_params.learning_neighbours || numberSelect;
            // typeSelect = parameters['iim'][dataAbbreviation].best_params.type_select || typeSelect;

            // M-RNN Parameters
            learningRate = parameters['mrnn'][dataAbbreviation].best_params.learning_rate || learningRate;
            hiddenDim = parameters['mrnn'][dataAbbreviation].best_params.hidden_dim || hiddenDim;
            iterationsMRNN = parameters['mrnn'][dataAbbreviation].best_params.iterations || iterationsMRNN;
            keepProb = parameters['mrnn'][dataAbbreviation].best_params.keep_prob || keepProb;
            // seqLen = parameters['iim'][dataAbbreviation].best_params.seq_len || seqLen;

            // ST-MVL Parameters
            windowSize = parameters['stmvl'][dataAbbreviation].best_params.window_size || windowSize;
            gamma = parameters['stmvl'][dataAbbreviation].best_params.gamma || gamma;
            alpha = parameters['stmvl'][dataAbbreviation].best_params.alpha || alpha;

            // }
          } catch (error) {
            naterq_error.value = true;
            console.error(error);
          }
        } else {
          // Set parameters to default (author's choice)
          truncationRank = String(CDREC_DEFAULTS.reductionValue);
          epsilon = String(CDREC_DEFAULTS.epsilon);
          iterations = CDREC_DEFAULTS.iterations;

          // IIM Parameters
          numberSelect = IIM_DEFAULTS.learningNeighbors;
          // typeSelect.value = 'mean';

          // M-RNN Parameters
          learningRate = MRNN_DEFAULTS.learningRate;
          hiddenDim = MRNN_DEFAULTS.hiddenDim;
          iterationsMRNN = MRNN_DEFAULTS.iterations;
          keepProb = MRNN_DEFAULTS.keepProb;
          // seqLen.value = 7;

          // ST-MVL Parameters
          windowSize = String(STMVL_DEFAULTS.windowSize);
          gamma = String(STMVL_DEFAULTS.gamma);
          alpha = String(STMVL_DEFAULTS.alpha);
        }
      }
    }


    function clearErrorMetrics() {
      rmseCDRec.value = null;
      maeCDRec.value = null;
      miCDRec.value = null;
      corrCDRec.value = null;

      rmseIIM.value = null;
      maeIIM.value = null;
      miIIM.value = null;
      corrIIM.value = null;

      rmseMRNN.value = null;
      maeMRNN.value = null;
      miMRNN.value = null;
      corrMRNN.value = null;

      rmseSTMVL.value = null;
      maeSTMVL.value = null;
      miSTMVL.value = null;
      corrSTMVL.value = null;
    }

    const handleCheckboxChange = async () => {

    if (dataSelect.value !== "upload")
    {
      loadingResults.value = true;
      imputedData.value = false;
      chartOptionsImputed.value.series.splice(0, chartOptionsImputed.value.series.length)
      chartOptionsOriginal.value.series.splice(0, chartOptionsOriginal.value.series.length)
      await fetchParameters();
      clearErrorMetrics();

      try
      {
        for (let checkedName of checkedNames.value)
        {
          const displayImputation = true

          let selection_series = ["-1:test"];
          if (selectedSeries.value.length > 0)
          {
              selection_series = selectedSeries.value;
          }

          obfuscatedMatrix.forEach((data: number[], index: number) => {
              chartOptionsImputed.value.series[index] = createSeries(index, data, dataSelect.value, currentSeriesNames[index], 'line', 5, obfuscatedColors[index]);
          });
          groundtruthMatrix.forEach((data: number[], index: number) => {
              if (selection_series.some(sel => sel.includes(currentSeriesNames[index].toString())))
              {
                chartOptionsImputed.value.series.push(createSeries(index, data, dataSelect.value,currentSeriesNames[index] + "_MV", 'dash', 5, obfuscatedColors[index], false));
              }
          });


          if (checkedName.toLowerCase() === 'cdrec')
          {
              if (!fetchedData[checkedName])
              {
                  const response = await axios.post('http://localhost:8000/api/cdrec/',
                      {
                        dataset: dataSelect.value,
                        normalization: normalizationMode.value,
                        scenario : scenarioMissingValues.value,
                        missing_rate : missingRate.value,
                        selected_series : selection_series,
                        truncation_rank: truncationRank,
                        epsilon: epsilon,
                        iterations: iterations,
                      },
                      {
                        headers: {
                          'Content-Type': 'application/json',
                        }
                      }
                  );
                  fetchedData[checkedName] = response.data;
              }

              rmseCDRec.value = fetchedData[checkedName].rmse.toFixed(3);
              maeCDRec.value = fetchedData[checkedName].mae.toFixed(3);
              miCDRec.value = fetchedData[checkedName].mi.toFixed(3);
              corrCDRec.value = fetchedData[checkedName].corr.toFixed(3);
              metricsCDRec.value = true;


              fetchedData[checkedName].matrix_imputed.forEach((data: number[], index: number) =>
              {
                if (selection_series.some(sel => sel.includes(currentSeriesNames[index].toString())))
                {
                  if (currentSeriesNames.length > 0 && currentSeriesNames[index])
                  {
                    if (displayImputation)
                    {
                      chartOptionsImputed.value.series.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], null, chartOptionsImputed.value, dataSelect.value, currentSeriesNames[index]+"_cdrec"));
                    }
                  }
                  else
                  {
                    if (displayImputation)
                    {
                      chartOptionsImputed.value.series.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], null, chartOptionsImputed.value, dataSelect.value, index+"_cdrec"));
                    }
                  }
                }
              });

              imputedData.value = true;
          }
          else if (checkedName.toLowerCase() == 'iim')
          {
              if (!fetchedData[checkedName])
              {
                const formattedAlgCode = `iim ${numberSelect}${typeSelect}`;
                const response = await axios.post('http://localhost:8000/api/iim/',
                    {
                      dataset: dataSelect.value,
                      normalization: normalizationMode.value,
                      scenario : scenarioMissingValues.value,
                      missing_rate : missingRate.value,
                      selected_series : selection_series,
                      alg_code: formattedAlgCode,
                    },
                    {
                      headers: {
                        'Content-Type': 'application/json',
                      }
                    }
                );
                fetchedData[checkedName] = response.data;
              }

              rmseIIM.value = fetchedData[checkedName].rmse.toFixed(3);
              maeIIM.value = fetchedData[checkedName].mae.toFixed(3);
              miIIM.value = fetchedData[checkedName].mi.toFixed(3);
              corrIIM.value = fetchedData[checkedName].corr.toFixed(3);
              metricsIIM.value = true;

              fetchedData[checkedName].matrix_imputed.forEach((data: number[], index: number) =>
              {
                if (selection_series.some(sel => sel.includes(currentSeriesNames[index].toString())))
                {
                  if (currentSeriesNames.length > 0 && currentSeriesNames[index])
                  {
                    if (displayImputation)
                    {
                      chartOptionsImputed.value.series.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], null, chartOptionsImputed.value, dataSelect.value, currentSeriesNames[index]+"_iim"));
                    }
                  }
                  else
                  {
                    if (displayImputation)
                    {
                      chartOptionsImputed.value.series.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], null, chartOptionsImputed.value, dataSelect.value, index+"_iim"));
                    }
                  }
                }
              });
              imputedData.value = true;
          }
          else if (checkedName.toLowerCase() === 'm-rnn')
          {
            if (!fetchedData[checkedName])
            {
              const response = await axios.post('http://localhost:8000/api/mrnn/',
                  {
                    dataset: dataSelect.value,
                    normalization: normalizationMode.value,
                    scenario : scenarioMissingValues.value,
                    missing_rate : missingRate.value,
                    selected_series : selection_series,
                    hidden_dim: hiddenDim,
                    learning_rate: learningRate,
                    iterations: iterationsMRNN,
                    keep_prob: keepProb,
                    seq_len: seqLen
                  },
                  {
                    headers: {
                      'Content-Type': 'application/json',
                    }
                  }
              );
              fetchedData[checkedName] = response.data;
            }

            rmseMRNN.value = fetchedData[checkedName].rmse.toFixed(3);
            maeMRNN.value = fetchedData[checkedName].mae.toFixed(3);
            miMRNN.value = fetchedData[checkedName].mi.toFixed(3);
            corrMRNN.value = fetchedData[checkedName].corr.toFixed(3);
            metricsMRNN.value = true;

            console.log("fetchedData[checkedName]", fetchedData[checkedName])
            console.log("rmseMRNN.value", rmseMRNN.value)
            console.log("fetchedData[checkedName].matrix_imputed", fetchedData[checkedName].matrix_imputed)
            console.log("obfuscatedMatrix", obfuscatedMatrix)

            fetchedData[checkedName].matrix_imputed.forEach((data: number[], index: number) =>
            {
              if (selection_series.some(sel => sel.includes(currentSeriesNames[index].toString())))
              {
                if (currentSeriesNames.length > 0 && currentSeriesNames[index])
                {
                  if (displayImputation)
                  {
                    chartOptionsImputed.value.series.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], null, chartOptionsImputed.value, dataSelect.value, currentSeriesNames[index]+"_mrnn"));
                  }
                }
                else
                {
                  if (displayImputation)
                  {
                    chartOptionsImputed.value.series.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], null, chartOptionsImputed.value, dataSelect.value, index+"_mrnn"));
                  }
                }
              }
            });
            imputedData.value = true;
          }
          else if (checkedName.toLowerCase() === 'st-mvl')
          {
            if (!fetchedData[checkedName]) {
              const response = await axios.post('http://localhost:8000/api/stmvl/',
                  {
                    dataset: dataSelect.value,
                    normalization: normalizationMode.value,
                    scenario : scenarioMissingValues.value,
                    missing_rate : missingRate.value,
                    selected_series : selection_series,
                    window_size: windowSize,
                    gamma: gamma,
                    alpha: alpha,
                  },
                  {
                    headers: {
                      'Content-Type': 'application/json',
                    }
                  }
              );
              fetchedData[checkedName] = response.data;
            }

            rmseSTMVL.value = fetchedData[checkedName].rmse.toFixed(3);
            maeSTMVL.value = fetchedData[checkedName].mae.toFixed(3);
            miSTMVL.value = fetchedData[checkedName].mi.toFixed(3);
            corrSTMVL.value = fetchedData[checkedName].corr.toFixed(3);
            metricsSTMVL.value = true;

            fetchedData[checkedName].matrix_imputed.forEach((data: number[], index: number) =>
            {
              if (selection_series.some(sel => sel.includes(currentSeriesNames[index].toString())))
              {
                if (currentSeriesNames.length > 0 && currentSeriesNames[index])
                {
                  if (displayImputation)
                  {
                    chartOptionsImputed.value.series.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], null, chartOptionsImputed.value, dataSelect.value, currentSeriesNames[index]+"_stmvl"));
                  }
                }
                else
                {
                  if (displayImputation)
                  {
                    chartOptionsImputed.value.series.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], null, chartOptionsImputed.value, dataSelect.value, index+"_stmvl"));
                  }
                }
              }
            });

            imputedData.value = true;
          }
        }

        mySeries.value = []
        for (let i = -1; i < currentSeriesNames.length && i < 4; i++)
        {
          mySeries.value.push(`${i + 1}: ${currentSeriesNames[i+1]}`);
        }

      } catch (error) {
        naterq_error.value = true;
        console.error(error);
      } finally {
        loadingResults.value = false;
      }
    }
    };

    const chartOptionsOriginal = ref(generateChartOptions('', 'Data'));
    const chartOptionsImputed = ref(generateChartOptions('', 'Data'));


    function showPopup()
    {
      document.getElementById('popup').style.display = 'block';
    }

    function closePopup()
    {
        document.getElementById('popup').style.display = 'none';
    }

    function printCheckedValues()
    {
        var nns_checkedv = document.getElementById('nns_based').checked;
        var reg_checkedv = document.getElementById('reg_based').checked;
        //var openFileChecked = document.getElementById('open_file_checkbox').checked;

        console.log("Pre-implemented checked nns_checked :", nns_checkedv);
        console.log("Pre-implemented checked reg_checked:", reg_checkedv);

        nns_checked.value = nns_checkedv
        reg_checked.value = reg_checkedv

    }


    function clearFetchedData()
    {
      for (let key in fetchedData)
      {
        delete fetchedData[key];
      }
    }

    function getCategory(dataSelectValue: string): string
    {
      if (dataSelectValue.startsWith('BAFU')) {
        return 'bafu';
      } else if (dataSelectValue.startsWith('cl2fullLarge')) {
        return 'chlorine';
      } else if (dataSelectValue.startsWith('climate')) {
        return 'climate';
      } else if (dataSelectValue.startsWith('batch10')) {
        return 'drift';
      } else if (dataSelectValue.startsWith('meteo')) {
        return 'meteo';
      } else {
        // If no match is found, return a default value (bafu) or throw an error
        return 'bafu';
      }
    }

    const submitForm = async () => {

      if (document.activeElement.id === "alpha_run")
      {
        imputedData.value = false;
        clearFetchedData();
        clearErrorMetrics();
        await handleCheckboxChange();
      }
      else if (document.activeElement.id === "upload_algo")
      {
        showPopup();
      }
       else if (document.activeElement.id === "validate")
      {
        printCheckedValues();
        closePopup();
      }
      else if (document.activeElement.id === "delta_reset")
      {
        location.reload();
      }
    }


    // Define a new function that calls fetchData
    const handleDataSelectChange = async () => {
      try {
        imputedData.value = false;
        clearFetchedData();
        await fetchData();
      } catch (error) {
        naterq_error.value = true;
        console.error("Error fetching data:", error);
      }
    }

    const updateSeriesNames = (newSeriesNames) => {
      currentSeriesNames = newSeriesNames;
    };

    const handleParamSelectChange = async () => {
      try
      {
        await fetchParameters();
        await submitForm();
      }
      catch (error)
      {
        naterq_error.value = true;
        console.error("Error handling parameter selection:", error);
      }
    }
      const handleNormalizationModeChange = () => {
      if (imputedData.value == true)
      {
          fetchData();
          submitForm();
      }
      else
      {
          handleDataSelectChange();
      }
    }


    const handleScenarioMissingValuesChange = () => {

      missingRate.value = "0";
      selectedSeries.value = [];

      if (imputedData.value == true)
      {
          fetchData();
          submitForm();
      }
      else
      {
          handleDataSelectChange();
      }
    }

    // Watch for changes and call fetchData when it changes
    watch([dataSelect, missingRate], handleDataSelectChange, {immediate: true});
    watch(normalizationMode, handleNormalizationModeChange, {immediate: true});
    watch(scenarioMissingValues, handleScenarioMissingValuesChange, {immediate: true});
    // Watch for changes and call fetchData when it changes
    // watch(selectedParamOption, handleParamSelectChange, {immediate: true});




    return {
      submitForm,
      // Error Metrics
      rmseCDRec,
      maeCDRec,
      miCDRec,
      corrCDRec,
      metricsCDRec,
      rmseIIM,
      maeIIM,
      miIIM,
      corrIIM,
      metricsIIM,
      rmseMRNN,
      maeMRNN,
      miMRNN,
      corrMRNN,
      metricsMRNN,
      rmseSTMVL,
      maeSTMVL,
      miSTMVL,
      corrSTMVL,
      metricsSTMVL,
      // End Error Metrics
      chartOptionsOriginal,
      chartOptionsImputed,
      dataSelect,
      normalizationMode,
      updateSeriesNames,
      missingRate,
      mySeries,
      selectedSeries,
      scenarioMissingValues,
      imputedData,
      checkedNames,
      handleCheckboxChange,
      // handleParamSelectChange,
      selectedParamOption,
      loadingResults,
      nns_checked,
      reg_checked,
      naterq_error
    }
  }
}


</script>
<style scoped>
.sidebar {
  margin-left: 35px; /* Change this value to increase or decrease the margin */
}
</style>

