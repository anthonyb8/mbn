use crate::enums::{Action, RType, Schema, Side};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyType;
use std::str::FromStr;

#[pymethods]
impl Side {
    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_cls: &Bound<'_, PyType>, value: char) -> PyResult<Self> {
        Side::try_from(value as u8)
            .map_err(|_| PyValueError::new_err(format!("Unknown Side value: '{}'", value)))
    }

    #[classmethod]
    fn from_int(_cls: &Bound<'_, PyType>, value: u8) -> PyResult<Self> {
        let char: char = value as char;
        Self::py_from_str(_cls, char)
    }

    fn __str__(&self) -> String {
        format!("{}", self)
    }

    fn __repr__(&self) -> String {
        format!("<Side.{}: '{}'>", self.name(), self.value())
    }

    #[getter]
    fn name(&self) -> String {
        self.as_ref().to_ascii_uppercase()
    }

    #[getter]
    fn value(&self) -> String {
        self.__str__()
    }
}

#[pymethods]
impl Action {
    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_cls: &Bound<'_, PyType>, value: char) -> PyResult<Self> {
        Action::try_from(value as u8)
            .map_err(|_| PyValueError::new_err(format!("Unknown Action value: '{}'", value)))
    }

    #[classmethod]
    pub fn from_int(_cls: &Bound<'_, PyType>, value: u8) -> PyResult<Self> {
        let char: char = value as char;
        Self::py_from_str(_cls, char)
    }

    fn __str__(&self) -> String {
        format!("{}", self)
    }

    fn __repr__(&self) -> String {
        format!("<Action.{}: '{}'>", self.name(), self.value())
    }

    #[getter]
    fn name(&self) -> String {
        self.as_ref().to_ascii_uppercase()
    }

    #[getter]
    fn value(&self) -> String {
        self.__str__()
    }
}

#[pymethods]
impl Schema {
    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_cls: &Bound<'_, PyType>, value: &Bound<PyAny>) -> PyResult<Self> {
        let schema_str: String = value.extract()?;
        Schema::from_str(&schema_str).map_err(|e| PyValueError::new_err(e.extract_message()))
    }

    fn __str__(&self) -> String {
        format!("{}", self)
    }
}

#[pymethods]
impl RType {
    #[classmethod]
    fn from_int(_cls: &Bound<'_, PyType>, value: u8) -> PyResult<Self> {
        RType::try_from(value)
            .map_err(|_| PyValueError::new_err(format!("Unknown RType value: {}", value)))
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_cls: &Bound<'_, PyType>, value: &str) -> PyResult<Self> {
        RType::from_str(value).map_err(|e| PyValueError::new_err(e.to_string()))
    }

    #[classmethod]
    fn from_schema(_cls: &Bound<'_, PyType>, value: &Bound<PyAny>) -> PyResult<Self> {
        let schema: Schema = value.extract()?;
        Ok(RType::from(schema))
    }

    fn __str__(&self) -> String {
        format!("{}", self)
    }
}
