package com.tarea4.tarea4.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class ActividadController {

    @GetMapping("/buscar-actividades")
    public String buscarActividades() {
        return "buscar-actividades";
    }
}