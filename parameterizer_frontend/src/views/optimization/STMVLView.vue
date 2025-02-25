<template>
  <h3 class="mb-4 text-center">ST-MVL Optimization</h3>
  <div class="d-flex mb-auto">
    <div class="col-lg-10">
      <div v-if="loadingResults" class="d-flex justify-content-center mt-3">
        <div class="alert alert-info d-flex align-items-center">
          <div class="spinner-border text-primary me-3" role="status"></div>
          Determining resulting imputation...
        </div>
      </div>
      <highcharts v-if="imputedData" :options="chartOptionsImputed"></highcharts>
      <div v-if="loadingParameters" class="d-flex justify-content-center mt-3">
        <div class="alert alert-info d-flex align-items-center">
          <div class="spinner-border text-primary me-3" role="status"></div>
          Determining optimal parameters...
        </div>
      </div>
      <form v-if="optimalParametersDetermined && imputedData" @submit.prevent="submitFormCustom"
            class="sidebar col-lg-3 align-items-center text-center">
        <h5>Optimal Parameters</h5>
<!--        <data-select-optimization v-model="dataSelect" @update:seriesNames="updateSeriesNames"/>-->

        <!--Window Size-->
        <div class="mb-3">
          <label for="windowSize" class="form-label">Window Size: {{ windowSize }}</label>
          <input id="windowSize" v-model.number="windowSize" type="range" min="2" max="100" step="1"
                 class="form-control">
        </div>

        <!--Smoothing Parameter Gamma-->
        <div class="mb-3">
          <label for="gamma" class="form-label">Smoothing Parameter (γ): {{ parseFloat(gamma).toFixed(5) }}</label>
          <input id="gamma" v-model.number="gamma" type="range" min="0.00005" max="0.99" step="0.00005"
                 class="form-control">
        </div>

        <!-- Power for Spatial Weight (Alpha) -->
        <div class="mb-3">
          <label for="alpha" class="form-label">Power for Spatial Weight (α): {{ alpha }}</label>
          <input id="alpha" v-model.number="alpha" type="range" min="0.5" max="20" step="0.5" class="form-control">
        </div>

        <button type="submit" class="btn btn-primary mr-3 mb-2">Impute</button>
        <br/>
        <button type="button" class="btn btn-secondary ml-3" @click="resetToOptimalParameters">Reset to Optimized</button>

      </form>
      <highcharts v-if="!imputedData" :options="chartOptionsOriginal"></highcharts>
    </div>
    <div class="col-lg-2">
      <form @submit.prevent="submitForm" class="sidebar me-3">
        <optimization-select v-model="optimizationSelect" @parametersChanged="handleParametersChanged"/>
        <data-select-optimization v-model="dataSelect" @update:seriesNames="updateSeriesNames"/>
        <!--        <missing-rate v-model="missingRate" />-->
        <normalization-toggle v-model="normalizationMode"></normalization-toggle>

        <br/>
        <button type="submit" class="btn btn-primary">Optimize</button>
        <div class="mt-3">
          <metrics-display v-if="imputedData" :metrics="metrics"></metrics-display>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import {ref, watch, computed} from 'vue';
import DataSelectOptimization from '../components/DataSelectOptimization.vue';
import MetricsDisplay from '../components/MetricsDisplay.vue';
import MissingRate from '../components/MissingRate.vue';
import NormalizationToggle from '../components/NormalizationToggleOptimization.vue'
import OptimizationSelect from '../components/OptimizationSelect.vue';
import axios from 'axios';
import {Chart} from 'highcharts-vue'
import Highcharts from 'highcharts'
import HighchartsBoost from 'highcharts/modules/boost'
import {
  createSegmentedSeries,
  createSeries,
  generateChartOptions,
  generateChartOptionsLarge
} from "@/views/thesisUtils/utils";

// HighchartsBoost(Highcharts)

export default {
  components: {
    DataSelectOptimization,
    highcharts: Chart,
    MetricsDisplay,
    MissingRate,
    NormalizationToggle,
    OptimizationSelect
  },
  setup() {
    const optimizationParameters = ref({}); // To store the optimization parameters received from the child component
    const dataSelect = ref('climate_eighth') // Default data
    const normalizationMode = ref('Normal')
    let currentSeriesNames = []; // Names of series currently displayed
    const missingRate = ref('10'); // Default missing rate
    const windowSize = ref('2'); // Default window size is 2
    const gamma = ref('0.5') // Default smoothing parameter gamma is 0.5, min 0.0, max 1.0
    const alpha = ref('2') // Default power for spatial weight (alpha) is 2, must be larger than 0.0
    const imputedData = ref(false); // Whether imputation has been carried out
    const rmse = ref(null);
    const mae = ref(null);
    const mi = ref(null);
    const corr = ref(null);
    const metrics = computed(() => ({rmse: rmse.value, mae: mae.value, mi: mi.value, corr: corr.value}));
    let optimalResponse: axios.AxiosResponse<any>;
    let optimalParametersDetermined = ref(false);
    let loadingParameters = ref(false);
    let loadingResults = ref(false);
    let obfuscatedMatrix = [];
    let groundtruthMatrix = [];

    const handleParametersChanged = (newParams: any) => {
      optimizationParameters.value = newParams; // Update the optimization parameters
    };

    const fetchData = async () => {
      imputedData.value = false;
      try {
        imputedData.value = false;
        let dataSet = `${dataSelect.value}_obfuscated_${missingRate.value}`;
        const response = await axios.post('http://localhost:8000/api/fetchData/',
            {
              data_set: dataSet,
              normalization: normalizationMode.value,
            },
            {
              headers: {
                'Content-Type': 'application/json',
              }
            }
        );
        chartOptionsOriginal.value.series.splice(0, chartOptionsOriginal.value.series.length);
        obfuscatedMatrix = response.data.matrix;
        groundtruthMatrix = response.data.groundtruth;
        response.data.matrix.forEach((data: number[], index: number) => {
          // Replace NaN with 0
          const cleanData = data.map(value => isNaN(value) ? 0 : value);

          if (currentSeriesNames.length > 0) {
            chartOptionsOriginal.value.series[index] = createSeries(index, cleanData, dataSelect.value, currentSeriesNames[index]);
          } else {
            chartOptionsOriginal.value.series[index] = createSeries(index, cleanData, dataSelect.value);
          }
        });
      } catch (error) {
        console.error(error);
      }
    }

    const submitForm = async () => {
      try {
        let dataSet = `${dataSelect.value}_obfuscated_10`;
        loadingParameters.value = true;
        imputedData.value = false;
        const response = await axios.post('http://localhost:8000/api/optimization/stmvl/',
            {
              ...optimizationParameters.value, // Spread the optimization parameters into the post body
              data_set: dataSet,
              normalization: normalizationMode.value,
              algorithm: 'stmvl'
            },
            {
              headers: {
                'Content-Type': 'application/json',
              }
            }
        );
        optimalResponse = response;
        gamma.value = response.data.best_params.gamma;
        alpha.value = response.data.best_params.alpha;
        windowSize.value = response.data.best_params.window_size;
        optimalParametersDetermined.value = true;
        loadingParameters.value = false;
        await submitFormCustom();
      } catch (error) {
        console.error(error);
      } finally {
        loadingParameters.value = false;
      }
    }


    const submitFormCustom = async () => {
      try {
        loadingResults.value = true;
        imputedData.value = false;
        let dataSet = `${dataSelect.value}_obfuscated_10`;
        const response = await axios.post('http://localhost:8000/api/stmvl/',
            {
              data_set: dataSet,
              normalization: normalizationMode.value,
              window_size: windowSize.value,
              gamma: gamma.value,
              alpha: alpha.value,
            },
            {
              headers: {
                'Content-Type': 'application/json',
              }
            }
        );
        rmse.value = response.data.rmse.toFixed(3);
        mae.value = response.data.mae.toFixed(3);
        mi.value = response.data.mi.toFixed(3);
        corr.value = response.data.corr.toFixed(3);
        chartOptionsImputed.value.series.length = 0;
        // Create a new array for the new series data
        const newSeriesData = [];

        const displayImputation = missingRate.value != '60' && missingRate.value != '80'
        response.data.matrix_imputed.forEach((data: number[], index: number) => {
          if (currentSeriesNames.length > 0 && missingRate) {
            if (displayImputation) {
              newSeriesData.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], groundtruthMatrix[index], chartOptionsImputed.value, dataSelect.value, currentSeriesNames[index]));
            } else {
              newSeriesData.push(createSeries(index, data, dataSelect.value, currentSeriesNames[index]));
            }
          } else {
            if (displayImputation) {
              newSeriesData.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], groundtruthMatrix[index], chartOptionsImputed.value, dataSelect.value));
            } else {
              newSeriesData.push(createSeries(index, data, dataSelect.value))
            }
          }
        });
        chartOptionsImputed.value.series = newSeriesData;
        imputedData.value = true;
      } catch (error) {
        console.error(error);
      } finally {
        loadingResults.value = false;
      }
    }


    const chartOptionsOriginal = ref(generateChartOptions('Original Data', 'Data'));
    const chartOptionsImputed = ref(generateChartOptionsLarge('Imputed Data', 'Data'));

    // Define a new function that calls fetchData
    const handleDataSelectChange = () => {
      chartOptionsImputed.value = generateChartOptionsLarge('Imputed Data', 'Data')
      fetchData();
    }

    const updateSeriesNames = (newSeriesNames) => {
      currentSeriesNames = newSeriesNames;
    };

    const handleNormalizationModeChange = () => {
      if (imputedData.value == true) {
          fetchData();
          submitFormCustom();
      } else {
          handleDataSelectChange();
      }
    }

    // Watch for changes and call fetchData when it changes
    watch([dataSelect, missingRate], handleDataSelectChange, {immediate: true});
    watch(normalizationMode, handleNormalizationModeChange, {immediate: true});

    const resetToOptimalParameters = () => {
      if (optimalResponse) {
        alpha.value = optimalResponse.data.best_params.alpha;
        gamma.value = optimalResponse.data.best_params.gamma;
        windowSize.value = optimalResponse.data.best_params.window_size;
      }
    }

    return {
      submitForm,
      submitFormCustom,
      metrics,
      chartOptionsOriginal,
      chartOptionsImputed,
      dataSelect,
      normalizationMode,
      updateSeriesNames,
      windowSize,
      gamma,
      alpha,
      missingRate,
      handleParametersChanged,
      optimalParametersDetermined,
      loadingParameters,
      resetToOptimalParameters,
      loadingResults,
      imputedData
    }
  }
}
</script>

<style scoped>
.sidebar {
  margin-left: 35px; /* Change this value to increase or decrease the margin */
}
</style>