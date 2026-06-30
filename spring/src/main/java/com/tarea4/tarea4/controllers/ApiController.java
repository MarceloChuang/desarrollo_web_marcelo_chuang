package com.tarea4.tarea4.controllers;

import com.tarea4.tarea4.models.Actividad;
import com.tarea4.tarea4.models.Nota;
import com.tarea4.tarea4.repositories.ActividadRepository;
import com.tarea4.tarea4.repositories.NotaRepository;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
public class ApiController {

    private final ActividadRepository actividadRepository;
    private final NotaRepository notaRepository;

    public ApiController(
            ActividadRepository actividadRepository,
            NotaRepository notaRepository
    ) {
        this.actividadRepository = actividadRepository;
        this.notaRepository = notaRepository;
    }

    @GetMapping("/api/actividades/buscar")
    public List<Map<String, Object>> buscarActividades(
            @RequestParam(name = "q", defaultValue = "") String q
    ) {
        String texto = q.trim();

        if (texto.length() < 3) {
            return List.of();
        }

        List<Actividad> actividades = actividadRepository.buscarPorTexto(texto);

        List<Map<String, Object>> respuesta = new ArrayList<>();

        for (Actividad actividad : actividades) {
            Double promedio = notaRepository.promedioPorActividad(actividad.getId());
            long cantidad = notaRepository.countByActividadId(actividad.getId());

            Map<String, Object> item = new HashMap<>();

            item.put("id", actividad.getId());
            item.put("nombre", actividad.getNombre());
            item.put("descripcion", actividad.getDescripcion());
            item.put("tipo", actividad.getTipo());
            item.put("dias", actividad.getDias());
            item.put("miembro", actividad.getMiembro().getNombreCompleto());
            item.put("comuna", actividad.getMiembro().getComuna().getNombre());

            if (promedio == null) {
                item.put("nota", "-");
                item.put("cantidad_notas", 0);
            } else {
                item.put("nota", Math.round(promedio * 10.0) / 10.0);
                item.put("cantidad_notas", cantidad);
            }

            respuesta.add(item);
        }

        return respuesta;
    }

    @PostMapping("/api/actividades/{id}/nota")
    public ResponseEntity<Map<String, Object>> agregarNota(
            @PathVariable Integer id,
            @RequestBody Map<String, Object> body
    ) {
        Object notaObjeto = body.get("nota");

        if (notaObjeto == null) {
            return ResponseEntity.badRequest().body(
                    Map.of("error", "Debe enviar una nota.")
            );
        }

        Integer valor;

        try {
            valor = Integer.parseInt(notaObjeto.toString());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(
                    Map.of("error", "La nota debe ser un número entero.")
            );
        }

        if (valor < 1 || valor > 7) {
            return ResponseEntity.badRequest().body(
                    Map.of("error", "La nota debe estar entre 1 y 7.")
            );
        }

        Optional<Actividad> actividadOptional = actividadRepository.findById(id);

        if (actividadOptional.isEmpty()) {
            return ResponseEntity.status(404).body(
                    Map.of("error", "La actividad no existe.")
            );
        }

        Actividad actividad = actividadOptional.get();

        Nota nuevaNota = new Nota(actividad, valor);
        notaRepository.save(nuevaNota);

        Double promedio = notaRepository.promedioPorActividad(id);
        long cantidad = notaRepository.countByActividadId(id);

        Map<String, Object> respuesta = new HashMap<>();
        respuesta.put("nota", Math.round(promedio * 10.0) / 10.0);
        respuesta.put("cantidad_notas", cantidad);

        return ResponseEntity.ok(respuesta);
    }
}